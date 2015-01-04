# Copyright (c) 2003-2014 CORE Security Technologies
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# $Id$
#
# Author: Alberto Solino (beto@coresecurity.com, bethus@gmail.com)
#
# Description:
#   Helper functions for kerberos
#   Just starting, TONS of things to do
#   In fact, make it easier
#

import datetime
import random
import socket
import struct
from pyasn1.codec.der import decoder, encoder
from impacket.krb5.asn1 import AS_REQ, AP_REQ, TGS_REQ, KERB_PA_PAC_REQUEST, KRB_ERROR, PA_ENC_TS_ENC, METHOD_DATA, AS_REP, TGS_REP, EncryptedData, Authenticator, EncASRepPart, EncTGSRepPart, seq_append, seq_set, seq_set_iter, seq_set_dict, KERB_ERROR_DATA, METHOD_DATA, ETYPE_INFO2_ENTRY, ETYPE_INFO_ENTRY, ETYPE_INFO2, ETYPE_INFO, AP_REP, EncAPRepPart
from impacket.krb5.types import KerberosTime, Principal, Ticket
from impacket.krb5.gssapi import CheckSumField, GSS_C_DCE_STYLE, GSS_C_DELEG_FLAG, GSS_C_MUTUAL_FLAG, GSS_C_REPLAY_FLAG, GSS_C_SEQUENCE_FLAG, GSS_C_CONF_FLAG, GSS_C_INTEG_FLAG 
from impacket.krb5 import constants
from impacket.krb5.crypto import _RC4, Key, _enctype_table
from impacket.smbconnection import SessionError
from impacket.spnego import SPNEGO_NegTokenInit, TypesMech, SPNEGO_NegTokenResp
from impacket.winregistry import hexdump
from impacket import nt_errors
from impacket.structure import Structure

def sendReceive(data, host, kdcHost):
    if kdcHost is None:
        targetHost = host
    else:
        targetHost = kdcHost

    messageLen = struct.pack('!i', len(data))

    s = socket.socket()
    s.connect((targetHost, 88))
    s.sendall(messageLen + data)

    recvDataLen = struct.unpack('!i', s.recv(4))[0]

    r = s.recv(recvDataLen)
    while len(r) < recvDataLen:
        r += s.recv(recvDataLen-len(r))

    try:
        krbError = KerberosError(packet = decoder.decode(r, asn1Spec = KRB_ERROR())[0])
    except:
        return r

    if krbError.getErrorCode() != constants.ErrorCodes.KDC_ERR_PREAUTH_REQUIRED.value:
        raise krbError

    return r

def getKerberosTGT(clientName, password, domain, lmhash, nthash, kdcHost, requestPAC=True):
    
    asReq = AS_REQ()

    domain = domain.upper()
    serverName = Principal('krbtgt/%s'%domain, type=constants.PrincipalNameType.NT_PRINCIPAL.value)  

    pacRequest = KERB_PA_PAC_REQUEST()
    pacRequest['include-pac'] = requestPAC
    encodedPacRequest = encoder.encode(pacRequest)

    asReq['pvno'] = 5
    asReq['msg-type'] =  int(constants.ApplicationTagNumbers.AS_REQ.value)
    asReq['padata'] = None
    asReq['padata'][0] = None
    asReq['padata'][0]['padata-type'] = int(constants.PreAuthenticationDataTypes.PA_PAC_REQUEST.value)
    asReq['padata'][0]['padata-value'] = encodedPacRequest

    reqBody = seq_set(asReq, 'req-body')

    opts = list()
    opts.append( constants.KDCOptions.forwardable.value )
    opts.append( constants.KDCOptions.renewable.value )
    opts.append( constants.KDCOptions.proxiable.value )
    reqBody['kdc-options']  = constants.encodeFlags(opts)

    seq_set(reqBody, 'sname', serverName.components_to_asn1)
    seq_set(reqBody, 'cname', clientName.components_to_asn1)

    if domain == '':
        raise 'Empty Domain not allowed in Kerberos'

    reqBody['realm'] = domain

    now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    reqBody['till'] = KerberosTime.to_asn1(now)
    reqBody['rtime'] = KerberosTime.to_asn1(now)
    reqBody['nonce'] =  random.SystemRandom().getrandbits(31)
    if nthash == '':
        # For now, I'll keep this commented, until I figure out 
        # a way to detect when a cypher is not accepted on the other 
        # end. I thought KDC_ERR_ETYPE_NOSUPP was enough, but I found
        # some systems that accepts it, and trigger an error when requesting
        # subsequent TGS :(. More research needed.
        #supportedCiphers = (int(constants.EncriptionTypes.rc4_hmac.value),
        #                   int(constants.EncriptionTypes.aes256_cts_hmac_sha1_96.value))
        supportedCiphers = (int(constants.EncriptionTypes.rc4_hmac.value),)
    else:
        # We have hashes to try, only way is to request RC4 only
        supportedCiphers = (int(constants.EncriptionTypes.rc4_hmac.value),)

    seq_set_iter(reqBody, 'etype', supportedCiphers)

    message = encoder.encode(asReq)

    r = sendReceive(message, domain, kdcHost)

    # This should be the PREAUTH_FAILED packet
    
    asRep = decoder.decode(r, asn1Spec = KRB_ERROR())[0]
    methods = decoder.decode(str(asRep['e-data']), asn1Spec=METHOD_DATA())[0]
    salt = ''
    encryptionTypesData = dict()
    for method in methods:
        if method['padata-type'] == constants.PreAuthenticationDataTypes.PA_ETYPE_INFO2.value:
            etypes2 = decoder.decode(str(method['padata-value']), asn1Spec = ETYPE_INFO2())[0]
            for etype2 in etypes2:
                if etype2['salt'] is None:
                    salt = ''
                else: 
                    salt = str(etype2['salt'])  
                encryptionTypesData[etype2['etype']] = salt
        elif method['padata-type'] == constants.PreAuthenticationDataTypes.PA_ETYPE_INFO.value:
            etypes = decoder.decode(str(method['padata-value']), asn1Spec = ETYPE_INFO())[0]
            for etype in etypes:
                if etype['salt'] is None:
                    salt = ''
                else: 
                    salt = str(etype['salt'])  
                encryptionTypesData[etype['etype']] = salt

    # Now let's cycle through all the available ciphers
    done = False
    for enctype in supportedCiphers:
        if encryptionTypesData.has_key(enctype) is False:
            continue

        # Let's build the timestamp
        timeStamp = PA_ENC_TS_ENC()

        now = datetime.datetime.utcnow() 
        timeStamp['patimestamp'] = KerberosTime.to_asn1(now)
        timeStamp['pausec'] = now.microsecond

        # Encrypt the shyte
        cipher = _enctype_table[enctype]
        if nthash != '':
            key = Key(cipher.enctype, nthash)
        else:
            key = cipher.string_to_key(password, encryptionTypesData[enctype], None)
        encodedTimeStamp = encoder.encode(timeStamp)

        # Key Usage 1
        # AS-REQ PA-ENC-TIMESTAMP padata timestamp, encrypted with the 
        # client key (Section 5.2.7.2)
        encriptedTimeStamp = cipher.encrypt(key, 1, encodedTimeStamp, None)

        encryptedData = EncryptedData()
        encryptedData['etype'] = cipher.enctype
        encryptedData['cipher'] = encriptedTimeStamp
        encodedEncryptedData = encoder.encode(encryptedData)

        # Now prepare the new AS_REQ again with the PADATA 
        # ToDo: cannot we reuse the previous one?
        asReq = AS_REQ()

        asReq['pvno'] = 5
        asReq['msg-type'] =  int(constants.ApplicationTagNumbers.AS_REQ.value)
        asReq['padata'] = None
        asReq['padata'][0] = None
        asReq['padata'][0]['padata-type'] = int(constants.PreAuthenticationDataTypes.PA_ENC_TIMESTAMP.value)
        asReq['padata'][0]['padata-value'] = encodedEncryptedData
 
        asReq['padata'][1] = None
        asReq['padata'][1]['padata-type'] = int(constants.PreAuthenticationDataTypes.PA_PAC_REQUEST.value)
        asReq['padata'][1]['padata-value'] = encodedPacRequest

        reqBody = seq_set(asReq, 'req-body')

        opts = list()
        opts.append( constants.KDCOptions.forwardable.value )
        opts.append( constants.KDCOptions.renewable.value )
        opts.append( constants.KDCOptions.proxiable.value )
        reqBody['kdc-options'] = constants.encodeFlags(opts)

        seq_set(reqBody, 'sname', serverName.components_to_asn1)
        seq_set(reqBody, 'cname', clientName.components_to_asn1)

        reqBody['realm'] =  domain

        now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        reqBody['till'] = KerberosTime.to_asn1(now)
        reqBody['rtime'] =  KerberosTime.to_asn1(now)
        reqBody['nonce'] = random.SystemRandom().getrandbits(31)

        seq_set_iter(reqBody, 'etype', ( (int(cipher.enctype),)))

        try:
            tgt = sendReceive(encoder.encode(asReq), domain, kdcHost) 
            done = True
        except Exception, e:
            if str(e).find('KDC_ERR_ETYPE_NOSUPP') < 0:
                raise e
            pass
        else:
            break        

    if done is False:
        # Something failed, let's trigger the error and leave
        tgt = sendReceive(encoder.encode(asReq), domain, kdcHost) 
    
    # So, we have the TGT, now extract the new session key and finish

    asRep = decoder.decode(tgt, asn1Spec = AS_REP())[0]
    cipherText = asRep['enc-part']['cipher']

    # Key Usage 3
    # AS-REP encrypted part (includes TGS session key or
    # application session key), encrypted with the client key
    # (Section 5.4.2)
    plainText = cipher.decrypt(key, 3, str(cipherText))
    encASRepPart = decoder.decode(plainText, asn1Spec = EncASRepPart())[0]

    # Get the session key and the ticket
    # We're assuming the cipher for this session key is the same
    # as the one we used before.
    # ToDo: change this
    sessionKey = Key(cipher.enctype,str(encASRepPart['key']['keyvalue']))

    # ToDo: Check Nonces!

    return tgt, cipher, key, sessionKey

def getKerberosTGS(serverName, domain, kdcHost, tgt, cipher, sessionKey):

    # Decode the TGT
    try:
        decodedTGT = decoder.decode(tgt, asn1Spec = AS_REP())[0]
    except:
        decodedTGT = decoder.decode(tgt, asn1Spec = TGS_REP())[0]

    domain = domain.upper()
    # Extract the ticket from the TGT
    ticket = Ticket()
    ticket.from_asn1(decodedTGT['ticket'])

    apReq = AP_REQ()
    apReq['pvno'] = 5
    apReq['msg-type'] = int(constants.ApplicationTagNumbers.AP_REQ.value)

    opts = list()
    apReq['ap-options'] =  constants.encodeFlags(opts)
    seq_set(apReq,'ticket', ticket.to_asn1)

    authenticator = Authenticator()
    authenticator['authenticator-vno'] = 5
    authenticator['crealm'] = str(decodedTGT['crealm'])

    clientName = Principal()
    clientName.from_asn1( decodedTGT, 'crealm', 'cname')

    seq_set(authenticator, 'cname', clientName.components_to_asn1)

    now = datetime.datetime.utcnow()
    authenticator['cusec'] =  now.microsecond
    authenticator['ctime'] = KerberosTime.to_asn1(now)

    encodedAuthenticator = encoder.encode(authenticator)

    # Key Usage 7
    # TGS-REQ PA-TGS-REQ padata AP-REQ Authenticator (includes
    # TGS authenticator subkey), encrypted with the TGS session
    # key (Section 5.5.1)
    encryptedEncodedAuthenticator = cipher.encrypt(sessionKey, 7, encodedAuthenticator, None)

    apReq['authenticator'] = None
    apReq['authenticator']['etype'] = cipher.enctype
    apReq['authenticator']['cipher'] = encryptedEncodedAuthenticator

    encodedApReq = encoder.encode(apReq)

    tgsReq = TGS_REQ()

    tgsReq['pvno'] =  5
    tgsReq['msg-type'] = int(constants.ApplicationTagNumbers.TGS_REQ.value)
    tgsReq['padata'] = None
    tgsReq['padata'][0] = None
    tgsReq['padata'][0]['padata-type'] = int(constants.PreAuthenticationDataTypes.PA_TGS_REQ.value)
    tgsReq['padata'][0]['padata-value'] = encodedApReq

    reqBody = seq_set(tgsReq, 'req-body')

    opts = list()
    opts.append( constants.KDCOptions.forwardable.value )
    opts.append( constants.KDCOptions.renewable.value )
    opts.append( constants.KDCOptions.renewable_ok.value )
    opts.append( constants.KDCOptions.canonicalize.value )

    reqBody['kdc-options'] = constants.encodeFlags(opts)
    seq_set(reqBody, 'sname', serverName.components_to_asn1)
    reqBody['realm'] = str(decodedTGT['crealm'])

    now = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    reqBody['till'] = KerberosTime.to_asn1(now)
    reqBody['nonce'] = random.SystemRandom().getrandbits(31)
    seq_set_iter(reqBody, 'etype',
                      (int(constants.EncriptionTypes.des3_cbc_sha1_kd.value),
                       int(cipher.enctype)))

    message = encoder.encode(tgsReq)

    r = sendReceive(message, domain, kdcHost)

    # Get the session key

    tgs = decoder.decode(r, asn1Spec = TGS_REP())[0]

    cipherText = tgs['enc-part']['cipher']

    # Key Usage 8
    # TGS-REP encrypted part (includes application session
    # key), encrypted with the TGS session key (Section 5.4.2)
    plainText = cipher.decrypt(sessionKey, 8, str(cipherText))

    encTGSRepPart = decoder.decode(plainText, asn1Spec = EncTGSRepPart())[0]

    newSessionKey = Key(cipher.enctype, str(encTGSRepPart['key']['keyvalue']))
    
    return r, cipher, sessionKey, newSessionKey

################################################################################
# DCE RPC Helpers
################################################################################
def getKerberosType3(cipher, sessionKey, auth_data):
    negTokenResp = SPNEGO_NegTokenResp(auth_data)
    # If DCE_STYLE = FALSE
    #ap_rep = decoder.decode(negTokenResp['ResponseToken'][16:], asn1Spec=AP_REP())[0]
    ap_rep = decoder.decode(negTokenResp['ResponseToken'], asn1Spec=AP_REP())[0]

    cipherText = str(ap_rep['enc-part']['cipher'])

    # Key Usage 12
    # AP-REP encrypted part (includes application session
    # subkey), encrypted with the application session key
    # (Section 5.5.2)
    plainText = cipher.decrypt(sessionKey, 12, cipherText)

    encAPRepPart = decoder.decode(plainText, asn1Spec = EncAPRepPart())[0]

    cipher = _enctype_table[int(encAPRepPart['subkey']['keytype'])]()
    sessionKey2 = Key(cipher.enctype, str(encAPRepPart['subkey']['keyvalue']))

    sequenceNumber = str(encAPRepPart['seq-number'])

    encAPRepPart['subkey'].clear()
    encAPRepPart = encAPRepPart.clone()

    now = datetime.datetime.utcnow()
    encAPRepPart['cusec'] = now.microsecond
    encAPRepPart['ctime'] = KerberosTime.to_asn1(now)
    encAPRepPart['seq-number'] = sequenceNumber
    encodedAuthenticator = encoder.encode(encAPRepPart)

    encryptedEncodedAuthenticator = cipher.encrypt(sessionKey, 12, encodedAuthenticator, None)

    ap_rep['enc-part'].clear()
    ap_rep['enc-part']['etype'] = cipher.enctype
    ap_rep['enc-part']['cipher'] = encryptedEncodedAuthenticator

    resp = SPNEGO_NegTokenResp()
    resp['ResponseToken'] = encoder.encode(ap_rep)

    return cipher, sessionKey2, resp.getData()

def getKerberosType1(username, password, domain, lmhash, nthash, targetName, kdcHost = None, TGT=None, TGS=None, ):
    # First of all, we need to get a TGT for the user
    userName = Principal(username, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
    if TGT is None:
        if TGS is None:
            tgt, cipher, oldSessionKey, sessionKey = getKerberosTGT(userName, password, domain, lmhash, nthash, kdcHost)
    else:
        tgt = TGT['KDC_REP']
        cipher = TGT['cipher']
        sessionKey = TGT['sessionKey'] 

    # Now that we have the TGT, we should ask for a TGS for cifs

    if TGS is None:
        serverName = Principal('LDAP/%s' % (targetName), type=constants.PrincipalNameType.NT_SRV_INST.value)
        tgs, cipher, oldSessionKey, sessionKey = getKerberosTGS(serverName, domain, kdcHost, tgt, cipher, sessionKey)
    else:
        tgs = TGS['KDC_REP']
        cipher = TGS['cipher']
        sessionKey = TGS['sessionKey'] 

    # Let's build a NegTokenInit with a Kerberos REQ_AP

    blob = SPNEGO_NegTokenInit() 

    # Kerberos
    blob['MechTypes'] = [TypesMech['MS KRB5 - Microsoft Kerberos 5']]

    # Let's extract the ticket from the TGS
    tgs = decoder.decode(tgs, asn1Spec = TGS_REP())[0]
    ticket = Ticket()
    ticket.from_asn1(tgs['ticket'])
    
    # Now let's build the AP_REQ
    apReq = AP_REQ()
    apReq['pvno'] = 5
    apReq['msg-type'] = int(constants.ApplicationTagNumbers.AP_REQ.value)

    opts = list()
    opts.append(constants.APOptions.mutual_required.value)
    apReq['ap-options'] = constants.encodeFlags(opts)
    seq_set(apReq,'ticket', ticket.to_asn1)

    authenticator = Authenticator()
    authenticator['authenticator-vno'] = 5
    authenticator['crealm'] = domain
    seq_set(authenticator, 'cname', userName.components_to_asn1)
    now = datetime.datetime.utcnow()

    authenticator['cusec'] = now.microsecond
    authenticator['ctime'] = KerberosTime.to_asn1(now)

    
    authenticator['cksum'] = None
    authenticator['cksum']['cksumtype'] = 0x8003

    chkField = CheckSumField()
    chkField['Lgth'] = 16

    chkField['Flags'] = GSS_C_CONF_FLAG | GSS_C_INTEG_FLAG | GSS_C_SEQUENCE_FLAG | GSS_C_REPLAY_FLAG | GSS_C_MUTUAL_FLAG | GSS_C_DCE_STYLE
    #chkField['Flags'] = GSS_C_INTEG_FLAG | GSS_C_SEQUENCE_FLAG | GSS_C_REPLAY_FLAG | GSS_C_MUTUAL_FLAG | GSS_C_DCE_STYLE
    authenticator['cksum']['checksum'] = chkField.getData()
    authenticator['seq-number'] = 0
    encodedAuthenticator = encoder.encode(authenticator)

    # Key Usage 11
    # AP-REQ Authenticator (includes application authenticator
    # subkey), encrypted with the application session key
    # (Section 5.5.1)
    encryptedEncodedAuthenticator = cipher.encrypt(sessionKey, 11, encodedAuthenticator, None)

    apReq['authenticator'] = None
    apReq['authenticator']['etype'] = cipher.enctype
    apReq['authenticator']['cipher'] = encryptedEncodedAuthenticator

    blob['MechToken'] = encoder.encode(apReq)

    return cipher, sessionKey, blob.getData()

class KerberosError(SessionError):
    """
    This is the exception every client should catch regardless of the underlying
    SMB version used. We'll take care of that. NETBIOS exceptions are NOT included,
    since all SMB versions share the same NETBIOS instances.
    """
    def __init__( self, error = 0, packet=0):
        SessionError.__init__(self)
        self.error = error
        self.packet = packet
        if packet != 0:
            self.error = self.packet['error-code']
       
    def getErrorCode( self ):
        return self.error

    def getErrorPacket( self ):
        return self.packet

    def getErrorString( self ):
        return constants.ERROR_MESSAGES[self.error]

    def __str__( self ):
        retString = 'Kerberos SessionError: %s(%s)' % (constants.ERROR_MESSAGES[self.error])
        try:
            # Let's try to get the NT ERROR, if not, we quit and give the general one
            if self.error == constants.ErrorCodes.KRB_ERR_GENERIC.value:
                eData = decoder.decode(str(self.packet['e-data']), asn1Spec = KERB_ERROR_DATA())[0]
                nt_error = struct.unpack('<L', str(eData['data-value'])[:4])[0]
                retString += '\nNT ERROR: %s(%s)' % (nt_errors.ERROR_MESSAGES[nt_error])
        except:
            pass

        return retString

