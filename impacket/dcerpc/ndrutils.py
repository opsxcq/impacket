# Copyright (c) 2003-2012 CORE Security Technologies
#
# This software is provided under under a slightly modified version
# of the Apache Software License. See the accompanying LICENSE file
# for more information.
#
# $Id$
#

from struct import *
import socket
import random
from impacket import uuid
from impacket import structure
from impacket.structure import *

def uuid_hex(_uuid):
    for i in range(0,len(_uuid)):
        print "\\0x%.2x"%unpack('<B',_uuid[i]),
    print ""

KNOWN_UUIDS = {
"\xb0\x01\x52\x97\xca\x59\xd0\x11\xa8\xd5\x00\xa0\xc9\x0d\x80\x51\x01\x00": "rpcss.dll",
"\xf1\x8f\x37\xc9\xf7\x16\xd0\x11\xa0\xb2\x00\xaa\x00\x61\x42\x6a\x01\x00": "pstorsvc.dll",
"\xd4\xa7\x72\x0d\x48\x61\xd1\x11\xb4\xaa\x00\xc0\x4f\xb6\x6e\xa0\x01\x00": "cryptsvc.dll",
"\x40\x4e\x9f\x8d\x3d\xa0\xce\x11\x8f\x69\x08\x00\x3e\x30\x05\x1b\x01\x00": "services.exe",
"\xc5\x86\x5a\xda\xc2\x12\x43\x49\xab\x30\x7f\x74\xa8\x13\xd8\x53\x01\x00": "regsvc.dll",
"\x29\x07\x8a\xfb\x04\x2d\x58\x46\xbe\x93\x27\xb4\xad\x55\x3f\xac\x01\x00": "lsass.exe",
"\x04\xf7\xd9\x52\xc6\xd3\x48\x47\xad\x11\x25\x50\x20\x9e\x80\xaf\x00\x00": "IMEPADSM.DLL",
"\xce\xad\x21\xc4\xb2\xa0\x0d\x48\x84\x18\x98\x44\x95\xb3\x2d\x5f\x01\x00": "SLsvc.exe",
"\x14\xb5\xfb\xd3\x3b\x0e\xcb\x11\x8f\xad\x08\x00\x2b\x1d\x29\xc3\x01\x00": "locator.exe",
"\x6f\x40\x1c\xf6\x60\xbd\x94\x41\x95\x65\xbf\xed\xd5\x25\x6f\x70\x01\x00": "p2phost.exe",
"\x72\x33\x3d\xc1\x20\xcc\x49\x44\x9b\x23\x8c\xc8\x27\x1b\x38\x85\x01\x00": "rpcrt4.dll",
"\x70\xfe\x5a\xd9\xd5\xa6\x59\x42\x82\x2e\x2c\x84\xda\x1d\xdb\x0d\x01\x00": "wininit.exe",
"\x6a\x07\x2d\x55\x29\xcb\x44\x4e\x8b\x6a\xd1\x5e\x59\xe2\xc0\xaf\x01\x00": "iphlpsvc.dll",
"\x95\x4f\x25\xd4\xc3\x08\xcc\x4f\xb2\xa6\x0b\x65\x13\x77\xa2\x9d\x01\x00": "wwansvc.dll",
"\x43\x9a\x89\x11\x68\x2b\x76\x4a\x92\xe3\xa3\xd6\xad\x8c\x26\xce\x01\x00": "lsm.exe",
"\xb4\x33\x6f\x26\xc1\xc7\xd1\x4b\x8f\x52\xdd\xb8\xf2\x21\x4e\xa9\x01\x00": "wlansvc.dll",
"\x68\x9d\xcb\x2a\x34\xb4\x3e\x4b\xb9\x66\xe0\x6b\x4b\x3a\x84\xcb\x01\x00": "bthserv.dll",
"\xd0\x4c\x67\x57\x00\x52\xce\x11\xa8\x97\x08\x00\x2b\x2e\x9c\x6d\x01\x00": "llssrv.exe",
"\x52\x44\x7d\x64\x33\x9f\x18\x4a\xb2\xbe\xc5\xc0\xe9\x20\xe9\x4e\x01\x00": "pla.dll",
"\xc8\x9b\x3b\xde\xf7\xbe\x78\x45\xa0\xde\xf0\x89\x04\x84\x42\xdb\x01\x00": "audiodg.exe",
"\xd1\x51\xa9\xbf\x0e\x2f\xd3\x11\xbf\xd1\x00\xc0\x4f\xa3\x49\x0a\x01\x00": "aqueue.dll",
"\x84\x55\x66\x1e\xfe\x40\x50\x44\x8f\x6e\x80\x23\x62\x39\x96\x94\x01\x00": "lsm.exe",
"\x41\x76\x17\xaa\x9b\xfc\xbd\x41\x80\xff\xf9\x64\xa7\x01\x59\x6f\x01\x00": "tssdis.exe",
"\xe0\x0c\x6b\x90\x0b\xc7\x67\x10\xb3\x17\x00\xdd\x01\x06\x62\xda\x01\x00": "msdtcprx.dll",
"\x51\xb9\x6b\xfd\x30\xc8\x34\x47\xbf\x2c\x18\xba\x6e\xc7\xab\x49\x01\x00": "iscsiexe.dll",
"\x68\xff\x1d\x62\x39\x3c\x6c\x4c\xaa\xe3\xe6\x8e\x2c\x65\x03\xad\x01\x00": "wzcsvc.dll",
"\x56\xcc\x35\x94\x9c\x1d\x24\x49\xac\x7d\xb6\x0a\x2c\x35\x20\xe1\x01\x00": "sppsvc.exe",
"\xf0\xe4\x9c\x36\xdc\x0f\xd3\x11\xbd\xe8\x00\xc0\x4f\x8e\xee\x78\x01\x00": "profmap.dll",
"\x6a\x28\x19\x39\x0c\xb1\xd0\x11\x9b\xa8\x00\xc0\x4f\xd9\x2e\xf5\x00\x00": "lsasrv.dll",
"\x80\x2b\xd1\x76\x67\x34\xd3\x11\x91\xff\x00\x90\x27\x2f\x9e\xa3\x01\x00": "mqqm.dll",
"\x72\xfe\x0f\x8d\x52\xd2\xd0\x11\xbf\x8f\x00\xc0\x4f\xd9\x12\x6b\x01\x00": "cryptsvc.dll",
"\x86\xd4\xdc\x68\x9e\x66\xd1\x11\xab\x0c\x00\xc0\x4f\xc2\xdc\xd2\x01\x00": "ismserv.exe",
"\x83\xaf\xe1\x1f\x5d\xc9\x11\x91\xa4\x08\x00\x2b\x14\xa0\xfa\x03\x00\x00": "rpcss.dll",
"\x06\x91\x01\x24\x03\xa2\x42\x46\xb8\x8d\x82\xda\xe9\x15\x89\x29\x01\x00": "authui.dll",
"\x60\xa7\xa4\x5c\xb1\xeb\xcf\x11\x86\x11\x00\xa0\x24\x54\x20\xed\x01\x00": "termsrv.dll",
"\x4d\xdd\x73\x34\x88\x2e\x06\x40\x9c\xba\x22\x57\x09\x09\xdd\x10\x05\x01": "winhttp.dll",
"\xb2\xb8\x7d\xb9\x63\x4c\xcf\x11\xbf\xf6\x08\x00\x2b\xe2\x3f\x2f\x02\x00": "clussvc.exe",
"\x95\x1f\x51\x33\x84\x5b\xcc\x4d\xb6\xcc\x3f\x4b\x21\xda\x53\xe1\x01\x00": "ubpm.dll",
"\x78\xb2\xeb\x05\x14\xe1\xc1\x4e\xa5\xa3\x09\x61\x53\xf3\x00\xe4\x01\x01": "tsgqec.dll",
"\x24\xe4\xfb\x63\x29\x20\xd1\x11\x8d\xb8\x00\xaa\x00\x4a\xbd\x5e\x01\x00": "Sens.dll",
"\x36\xa0\x67\x07\x22\x0d\xaa\x48\xba\x69\xb6\x19\x48\x0f\x38\xcb\x01\x00": "pcasvc.dll",
"\x20\x32\x5f\x2f\x26\xc1\x76\x10\xb5\x49\x07\x4d\x07\x86\x19\xda\x01\x00": "netdde.exe",
"\x30\xa0\xb3\xfd\x5f\x06\xd1\x11\xbb\x9b\x00\xa0\x24\xea\x55\x25\x01\x00": "mqqm.dll",
"\x80\x7a\xdf\x77\x98\xf2\xd0\x11\x83\x58\x00\xa0\x24\xc4\x80\xa8\x01\x00": "mqdssrv.dll",
"\x03\x6d\x71\x98\xac\x89\xc7\x44\xbb\x8c\x28\x58\x24\xe5\x1c\x4a\x01\x00": "srvsvc.dll",
"\xc8\xad\x32\x4f\x52\x60\x04\x4a\x87\x01\x29\x3c\xcf\x20\x96\xf0\x01\x00": "sspisrv.dll",
"\x90\x38\xa9\x65\xb9\xfa\xa3\x43\xb2\xa5\x1e\x33\x0a\xc2\x8f\x11\x02\x00": "dnsrslvr.dll",
"\x32\xf5\x03\xc5\x3a\x44\x69\x4c\x83\x00\xcc\xd1\xfb\xdb\x38\x39\x01\x00": "MpSvc.dll",
"\x46\x9f\x3b\xc3\x88\x20\xbc\x4d\x97\xe3\x61\x25\xf1\x27\x66\x1c\x01\x00": "nlasvc.dll",
"\xa0\xb3\x02\xa0\xb7\xc9\xd1\x11\xae\x88\x00\x80\xc7\x5e\x4e\xc1\x01\x00": "wlnotify.dll",
"\xd0\xd1\x33\x88\x5f\x96\x16\x42\xb3\xe9\xfb\xe5\x8c\xad\x31\x00\x01\x00": "SCardSvr.dll",
"\x98\xd0\xff\x6b\x12\xa1\x10\x36\x98\x33\x46\xc3\xf8\x7e\x34\x5a\x01\x00": "wkssvc.dll",
"\x38\x8d\x04\x7e\x08\xac\xf1\x4f\x8e\x6b\xf3\x5d\xba\xb8\x8d\x4a\x01\x00": "mqqm.dll",
"\x35\x42\x51\xe3\x06\x4b\xd1\x11\xab\x04\x00\xc0\x4f\xc2\xdc\xd2\x04\x00": "ntdsai.dll",
"\xc8\x4f\x32\x4b\x70\x16\xd3\x01\x12\x78\x5a\x47\xbf\x6e\xe1\x88\x00\x00": "sfmsvc.exe",
"\xc5\x28\x47\x3c\xab\xf0\x8b\x44\xbd\xa1\x6c\xe0\x1e\xb0\xa6\xd6\x01\x00": "dhcpcsvc6.dll",
"\x36\x01\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x46\x00\x00": "rpcss.dll",
"\x54\x79\x26\x3d\xb7\xee\xd1\x11\xb9\x4e\x00\xc0\x4f\xa3\x08\x0d\x01\x00": "lserver.dll",
"\xbf\x09\x11\x81\xe1\xa4\xd1\x11\xab\x54\x00\xa0\xc9\x1e\x9b\x45\x01\x00": "WINS.EXE",
"\xd0\xbb\xf5\x7a\x63\x60\xd1\x11\xae\x2a\x00\x80\xc7\x5e\x4e\xc1\x00\x00": "irmon.dll",
"\x99\x1e\xb8\x12\x07\xf2\x4c\x4a\x85\xd3\x77\xb4\x2f\x76\xfd\x14\x01\x00": "seclogon.dll",
"\x6c\x5e\x64\x00\x9f\xfc\x0c\x4a\x98\x96\xf0\x0b\x66\x29\x77\x98\x01\x00": "icardagt.exe",
"\x9f\x2f\x5b\xb1\x3c\x90\x71\x46\x8d\xc0\x77\x2c\x54\x21\x40\x68\x01\x00": "pwmig.dll",
"\xa6\x95\x7d\x49\x27\x2d\xf5\x4b\x9b\xbd\xa6\x04\x69\x57\x13\x3c\x01\x00": "termsrv.dll",
"\xcb\x92\xbe\x5c\xbe\xf4\xc9\x45\x9f\xc9\x33\xe7\x3e\x55\x7b\x20\x01\x00": "lsasrv.dll",
"\xa1\x0f\x51\x69\x99\x2f\xeb\x4e\xa4\xff\xaf\x25\x9f\x0f\x97\x49\x01\x00": "wecsvc.dll",
"\x70\x5d\xfb\x8c\xa4\x31\xcf\x11\xa7\xd8\x00\x80\x5f\x48\xa1\x35\x03\x00": "smtpsvc.dll",
"\x46\x0d\x85\x77\x1d\x85\xb6\x43\x93\x98\x29\x01\x61\xf0\xca\xe6\x01\x00": "SeVA.dll",
"\xc3\x26\xf2\x76\x14\xec\x25\x43\x8a\x99\x6a\x46\x34\x84\x18\xaf\x01\x00": "winlogon.exe",
"\x84\x65\x0a\x0b\x0f\x9e\xcf\x11\xa3\xcf\x00\x80\x5f\x68\xcb\x1b\x01\x00": "rpcss.dll",
"\x15\x55\xf2\x11\x79\xc8\x0a\x40\x98\x9e\xb0\x74\xd5\xf0\x92\xfe\x01\x00": "lsm.exe",
"\xc0\xe0\x4d\x89\x55\x0d\xd3\x11\xa3\x22\x00\xc0\x4f\xa3\x21\xa1\x01\x00": "wininit.exe",
"\x00\xac\x0a\xf5\xf3\xc7\x8e\x42\xa0\x22\xa6\xb7\x1b\xfb\x9d\x43\x01\x00": "cryptsvc.dll",
"\xa5\x44\xb0\x30\x25\xa2\xf0\x43\xb3\xa4\xe0\x60\xdf\x91\xf9\xc1\x01\x00": "certprop.dll",
"\x78\x57\x34\x12\x34\x12\xcd\xab\xef\x00\x01\x23\x45\x67\x89\xab\x00\x00": "lsasrv.dll",
"\x49\x69\xe9\x98\x59\xbc\xf1\x47\x92\xd1\x8c\x25\xb4\x6f\x85\xc7\x01\x00": "wlanext.exe",
"\xb8\x61\xe5\xff\x15\xbf\xcf\x11\x8c\x5e\x08\x00\x2b\xb4\x96\x49\x02\x00": "clussvc.exe",
"\xb4\x59\xcc\xf5\x64\x42\x1a\x10\x8c\x59\x08\x00\x2b\x2f\x84\x26\x01\x00": "ntfrs.exe",
"\xb4\x59\xcc\xf5\x64\x42\x1a\x10\x8c\x59\x08\x00\x2b\x2f\x84\x26\x01\x01": "ntfrs.exe",
"\xa4\xc2\xab\x50\x4d\x57\xb3\x40\x9d\x66\xee\x4f\xd5\xfb\xa0\x76\x05\x00": "dns.exe",
"\xb9\x99\x3f\x87\x4d\x1b\x10\x99\xb7\xaa\x00\x04\x00\x7f\x07\x01\x00\x00": "ssmsrp70.dll",
"\x01\xc3\x53\xb2\xa2\x78\x70\x42\xa9\x1f\x66\x0d\xee\x06\x9f\x4c\x01\x00": "rdpcore.dll",
"\x94\x68\x71\x22\x8e\xfd\x62\x44\x97\x83\x09\xe6\xd9\x53\x1f\x16\x01\x00": "ubpm.dll",
"\xf6\xb8\x35\xd3\x31\xcb\xd0\x11\xb0\xf9\x00\x60\x97\xba\x4e\x54\x01\x00": "polagent.dll",
"\x64\x1d\x82\x0c\xfc\xa3\xd1\x11\xbb\x7a\x00\x80\xc7\x5e\x4e\xc1\x01\x00": "irftp.exe",
"\xb8\x4a\x9f\x4d\x1c\x7d\xcf\x11\x86\x1e\x00\x20\xaf\x6e\x7c\x57\x00\x00": "rpcss.dll",
"\xa8\x95\xee\x81\x2e\x88\x15\x46\x88\x8a\x53\x34\x4c\xa1\x49\xe4\x01\x00": "vpnikeapi.dll",
"\xfb\xee\x0c\x13\x66\xe4\xd1\x11\xb7\x8b\x00\xc0\x4f\xa3\x28\x83\x02\x00": "ismip.dll",
"\x72\xee\xf3\xc6\x7e\xce\xd1\x11\xb7\x1e\x00\xc0\x4f\xc3\x11\x1a\x01\x00": "rpcss.dll",
"\x9a\xf9\x1e\x20\xa0\x7f\x4c\x44\x93\x99\x19\xba\x84\xf1\x2a\x1a\x01\x00": "appinfo.dll",
"\xc8\x4f\x32\x4b\x70\x16\xd3\x01\x12\x78\x5a\x47\xbf\x6e\xe1\x88\x03\x00": "srvsvc.dll",
"\x72\xe4\x9f\x6d\xf1\x30\x08\x47\x8f\xa8\x67\x83\x62\xb9\x61\x55\x01\x00": "wimserv.exe",
"\xd4\xd7\x44\x7c\xd5\x31\x4c\x42\xbd\x5e\x2b\x3e\x1f\x32\x3d\x22\x01\x00": "ntdsai.dll",
"\x55\x1a\x20\x6f\x4d\xa2\x5f\x49\xaa\xc9\x2f\x4f\xce\x34\xdf\x99\x01\x00": "IPHLPAPI.DLL",
"\x32\x35\x0f\x30\xcc\x38\xd0\x11\xa3\xf0\x00\x20\xaf\x6b\x0a\xdd\x01\x02": "trkwks.dll",
"\x32\x35\x0f\x30\xcc\x38\xd0\x11\xa3\xf0\x00\x20\xaf\x6b\x0a\xdd\x01\x00": "trkwks.dll",
"\x60\xf4\x82\x4f\x21\x0e\xcf\x11\x90\x9e\x00\x80\x5f\x48\xa1\x35\x04\x00": "nntpsvc.dll",
"\x7d\xce\x54\x5f\x79\x5b\x75\x41\x85\x84\xcb\x65\x31\x3a\x0e\x98\x01\x00": "appinfo.dll",
"\xdc\x3f\x27\x82\x2a\xe3\xc3\x18\x3f\x78\x82\x79\x29\xdc\x23\xea\x00\x00": "wevtsvc.dll",
"\x3a\xcf\xe0\x16\x04\xa6\xd0\x11\x96\xb1\x00\xa0\xc9\x1e\xce\x30\x01\x00": "ntdsbsrv.dll",
"\x98\xd0\xff\x6b\x12\xa1\x10\x36\x98\x33\x01\x28\x92\x02\x01\x62\x00\x00": "browser.dll",
"\xd6\x09\x48\x48\x39\x42\x1b\x47\xb5\xbc\x61\xdf\x8c\x23\xac\x48\x01\x00": "lsm.exe",
"\xe8\x04\xe6\x58\xdb\x9a\x2e\x4d\xa4\x64\x3b\x06\x83\xfb\x14\x80\x01\x00": "appinfo.dll",
"\x57\x72\xd4\xa2\xf7\x12\xeb\x4b\x89\x81\x0e\xbf\xa9\x35\xc4\x07\x01\x00": "p2psvc.dll",
"\x1e\xdd\x5b\x6b\x8c\x52\x2c\x42\xaf\x8c\xa4\x07\x9b\xe4\xfe\x48\x01\x00": "FwRemoteSvr.dll",
"\x75\x21\xc8\x51\x4e\x84\x50\x47\xb0\xd8\xec\x25\x55\x55\xbc\x06\x01\x00": "SLsvc.exe",
"\x78\x57\x34\x12\x34\x12\xcd\xab\xef\x00\x01\x23\x45\x67\x89\xac\x01\x00": "samsrv.dll",
"\xc0\x47\xdf\xb3\x5a\xa9\xcf\x11\xaa\x26\x00\xaa\x00\xc1\x48\xb9\x09\x00": "mspadmin.exe - Microsoft ISA Server",
"\x00\xac\x0a\xf5\xf3\xc7\x8e\x42\xa0\x22\xa6\xb7\x1b\xfb\x9d\x43\x01\x01": "cryptsvc.dll",
"\x65\x31\x0a\xea\x34\x48\xd2\x11\xa6\xf8\x00\xc0\x4f\xa3\x46\xcc\x04\x00": "FXSSVC.exe",
"\x33\xa2\x74\xd6\x29\x58\xdd\x49\x90\xf0\x60\xcf\x9c\xeb\x71\x29\x01\x00": "ipnathlp.dll",
"\xf7\xaf\xbe\xf6\x19\x1e\xbb\x4f\x9f\x8f\xb8\x9e\x20\x18\x33\x7c\x01\x00": "wevtsvc.dll",
"\x70\x0d\xec\xec\x03\xa6\xd0\x11\x96\xb1\x00\xa0\xc9\x1e\xce\x30\x02\x00": "ntdsbsrv.dll",
"\x7c\xda\x83\x4f\xe8\xd2\x11\x98\x07\x00\xc0\x4f\x8e\xc8\x50\x02\x00\x00": "sfc.dll",
"\x80\x92\xea\x46\xbf\x5b\x5e\x44\x83\x1d\x41\xd0\xf6\x0f\x50\x3a\x01\x00": "ifssvc.exe",
"\x81\xbb\x7a\x36\x44\x98\xf1\x35\xad\x32\x98\xf0\x38\x00\x10\x03\x02\x00": "services.exe",
"\x66\x9f\x9b\x62\x6c\x55\xd1\x11\x8d\xd2\x00\xaa\x00\x4a\xbd\x5e\x03\x00": "sens.dll",
"\x1c\x02\x0c\xa0\xe2\x2b\xd2\x11\xb6\x78\x00\x00\xf8\x7a\x8f\x8e\x01\x00": "ntfrs.exe",
"\x3e\xca\x86\xc3\x61\x90\x72\x4a\x82\x1e\x49\x8d\x83\xbe\x18\x8f\x01\x01": "audiosrv.dll",
"\x6d\xa5\x6e\xe7\x3f\x45\xcf\x11\xbf\xec\x08\x00\x2b\xe2\x3f\x2f\x02\x01": "resrcmon.exe",
"\xe1\xbf\x72\x4a\x94\x92\xda\x11\xa7\x2b\x08\x00\x20\x0c\x9a\x66\x01\x00": "rdpinit.exe",
"\x7c\x5f\xc4\xa2\x32\x7d\xad\x46\x96\xf5\xad\xaf\xb4\x86\xbe\x74\x01\x00": "services.exe",
"\x01\x6b\x77\x45\x56\x59\x85\x44\x9f\x80\xf4\x28\xf7\xd6\x01\x29\x02\x00": "dnsrslvr.dll",
"\x96\x7b\x9b\x6c\xa8\x45\xca\x4c\x9e\xb3\xe2\x1c\xcf\x8b\x5a\x89\x01\x00": "umpo.dll",
"\x15\x04\x42\x9d\xfb\xb8\x4a\x4f\x8c\x53\x45\x02\xea\xd3\x0c\xa9\x01\x00": "PlaySndSrv.dll",
"\x50\x38\xcd\x15\xca\x28\xce\x11\xa4\xe8\x00\xaa\x00\x61\x16\xcb\x01\x00": "PeerDistSvc.dll",
"\x20\xe5\x98\xa3\x9a\xd5\xdd\x4b\xaa\x7a\x3c\x1e\x03\x03\xa5\x11\x01\x00": "IKEEXT.DLL",
"\x08\x83\xaf\xe1\x1f\x5d\xc9\x11\x91\xa4\x08\x00\x2b\x14\xa0\xfa\x03\x00": "rpcss.dll",
"\x00\x7c\xda\x83\x4f\xe8\xd2\x11\x98\x07\x00\xc0\x4f\x8e\xc8\x50\x02\x00": "sfc_os.dll",
"\xf2\xdc\x51\x4a\x3a\x5c\xd2\x4d\x84\xdb\xc3\x80\x2e\xe7\xf9\xb7\x01\x00": "ntdsai.dll",
"\x82\x06\xf7\x1f\x51\x0a\xe8\x30\x07\x6d\x74\x0b\xe8\xce\xe9\x8b\x01\x00": "taskcomp.dll",
"\x00\xb9\x99\x3f\x87\x4d\x1b\x10\x99\xb7\xaa\x00\x04\x00\x7f\x07\x01\x00": "ssmsrpc.dll - Microsoft SQL Server",
"\x20\x17\x82\x5b\x3b\xf6\xd0\x11\xaa\xd2\x00\xc0\x4f\xc3\x24\xdb\x01\x00": "dhcpssvc.dll",
"\x22\xc4\xa1\x4d\x3d\x94\xd1\x11\xac\xae\x00\xc0\x4f\xc2\xaa\x3f\x01\x00": "trksvr.dll",
"\x74\xe9\xa5\x1a\x82\x62\x8d\x4e\x9c\x96\x40\x18\x6e\x89\xd2\x80\x01\x00": "scss.exe",
"\x94\x73\x92\x1a\x2e\x35\x53\x45\xae\x3f\x7c\xf4\xaa\xfc\xa6\x20\x01\x00": "wdssrv.dll",
"\x66\xf6\x8c\x04\x42\xab\xb4\x42\x89\x75\x13\x57\x01\x8d\xec\xb3\x01\x00": "ws2_32.dll",
"\x3a\xcf\xe0\x16\x04\xa6\xd0\x11\x96\xb1\x00\xa0\xc9\x1e\xce\x30\x02\x00": "ntdsbsrv.dll",
"\x02\x00\x00\x00\x01\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x69\x01\x00": "kdcsvc.dll",
"\xb0\x52\x8e\x37\xa9\xc0\xcf\x11\x82\x2d\x00\xaa\x00\x51\xe4\x0f\x01\x00": "taskcomp.dll",
"\xe0\x6d\x7a\x8c\x8d\x78\xd0\x11\x9e\xdf\x44\x45\x53\x54\x00\x00\x02\x00": "wiaservc.dll",
"\x05\x81\xa7\x3c\xa3\xa3\x68\x4a\xb4\x58\x1a\x60\x6b\xab\x8f\xd6\x01\x00": "mpnotify.exe",
"\x2e\xa0\x8a\xb5\x84\x28\x97\x4e\x81\x76\x4e\xe0\x6d\x79\x41\x84\x01\x00": "sysmain.dll",
"\x95\x4f\x25\xd4\xc3\x08\xcc\x4f\xb2\xa6\x0b\x65\x13\x77\xa2\x9c\x01\x00": "wwansvc.dll",
"\x6e\x2c\xf4\xc3\xcc\xd4\x5a\x4e\x93\x8b\x9c\x5e\x8a\x5d\x8c\x2e\x01\x00": "wlanmsm.dll",
"\x53\x0c\x19\xf3\x0c\x4e\x1a\x49\xaa\xd3\x2a\x7c\xeb\x7e\x25\xd4\x01\x00": "vpnikeapi.dll",
"\x26\xc0\xe1\xac\x3f\x8b\x11\x47\x89\x18\xf3\x45\xd1\x7f\x5b\xff\x01\x00": "lsasrv.dll",
"\xc0\xc4\x55\xae\xce\x64\xdd\x11\xad\x8b\x08\x00\x20\x0c\x9a\x66\x01\x00": "bdesvc.dll",
"\xc4\x0c\x3c\xe3\x82\x04\x1a\x10\xbc\x0c\x02\x60\x8c\x6b\xa2\x18\x01\x00": "locator.exe",
"\x0e\x3b\x6c\x50\xd1\x4b\x56\x4c\x88\xc0\x49\xa2\x0e\xd4\xb5\x39\x01\x00": "milcore.dll",
"\x3e\x8e\xb0\x2e\x9f\x63\xba\x4f\x97\xb1\x14\xf8\x78\x96\x10\x76\x01\x00": "gpsvc.dll",
"\x66\x9f\x9b\x62\x6c\x55\xd1\x11\x8d\xd2\x00\xaa\x00\x4a\xbd\x5e\x02\x00": "sens.dll",
"\xb5\x6d\xac\xc9\xb7\x82\x55\x4e\xae\x8a\xe4\x64\xed\x7b\x42\x77\x01\x00": "sysntfy.dll",
"\x98\x46\xbc\xa0\xd7\xb8\x30\x43\xa2\x8f\x77\x09\xe1\x8b\x61\x08\x04\x00": "Sens.dll",
"\x1e\xc9\x31\x3f\x45\x25\x7b\x4b\x93\x11\x95\x29\xe8\xbf\xfe\xf6\x01\x00": "p2psvc.dll",
"\x3e\xca\x86\xc3\x61\x90\x72\x4a\x82\x1e\x49\x8d\x83\xbe\x18\x8f\x02\x00": "audiosrv.dll",
"\x3e\xca\x86\xc3\x61\x90\x72\x4a\x82\x1e\x49\x8d\x83\xbe\x18\x8f\x02\x02": "audiosrv.dll",
"\xf8\x91\x7b\x5a\x00\xff\xd0\x11\xa9\xb2\x00\xc0\x4f\xb6\xe6\xfc\x01\x00": "msgsvc.dll",
"\x98\xd0\xff\x6b\x12\xa1\x10\x36\x98\x33\x46\xc3\xf8\x74\x53\x2d\x01\x00": "dhcpssvc.dll",
"\xb8\xd0\x48\xe2\x15\xbf\xcf\x11\x8c\x5e\x08\x00\x2b\xb4\x96\x49\x02\x00": "clussvc.exe",
"\x78\xad\xbc\x1c\x0b\xdf\x34\x49\xb5\x58\x87\x83\x9e\xa5\x01\xc9\x00\x00": "lsasrv.dll",
"\x87\x76\xcb\xc8\xd3\xe6\xd2\x11\xa9\x58\x00\xc0\x4f\x68\x2e\x16\x01\x00": "WebClnt.dll",
"\x88\xd4\x81\xc6\x50\xd8\xd0\x11\x8c\x52\x00\xc0\x4f\xd9\x0f\x7e\x01\x00": "lsasrv.dll",
"\x80\x35\x5b\x5b\xe0\xb0\xd1\x11\xb9\x2d\x00\x60\x08\x1e\x87\xf0\x01\x00": "mqqm.dll",
"\xf0\x09\x8f\xed\xb7\xce\x11\xbb\xd2\x00\x00\x1a\x18\x1c\xad\x00\x00\x00": "mprdim.dll",
"\xd8\x5d\xe6\x12\x7f\x88\xef\x41\x91\xbf\x8d\x81\x6c\x42\xc2\xe7\x01\x00": "winlogon.exe",
"\xf8\x91\x7b\x5a\x00\xff\xd0\x11\xa9\xb2\x00\xc0\x4f\xb6\x36\xfc\x01\x00": "msgsvc.dll",
"\x01\xd0\x8c\x33\x44\x22\xf1\x31\xaa\xaa\x90\x00\x38\x00\x10\x03\x01\x00": "regsvc.dll",
"\x03\xd7\xfd\x17\x27\x18\x34\x4e\x79\xd4\x24\xa5\x5c\x53\xbb\x37\x01\x00": "msgsvc.dll",
"\x1c\x95\x57\x33\xd1\xa1\xdb\x47\xa2\x78\xab\x94\x5d\x06\x3d\x03\x01\x00": "LBService.dll",
"\xab\xbe\x00\xc1\x3a\xd3\x4b\x4a\xbf\x23\xbb\xef\x46\x63\xd0\x17\x01\x00": "wcncsvc.dll",
"\xc4\xfc\x7b\x82\xb4\x38\xcd\x4a\x92\xe4\x21\xe1\x50\x6b\x85\xfb\x01\x00": "SLsvc.exe",
"\x00\xf0\x09\x8f\xed\xb7\xce\x11\xbb\xd2\x00\x00\x1a\x18\x1c\xad\x00\x00": "mprdim.dll",
"\x4b\xa0\x12\x72\x63\xb4\x2e\x40\x96\x49\x2b\xa4\x77\x39\x46\x76\x01\x00": "umrdp.dll",
"\x20\x65\x5f\x2f\x46\xca\x67\x10\xb3\x19\x00\xdd\x01\x06\x62\xda\x01\x00": "tapisrv.dll",
"\xa0\x9e\xc0\x69\x09\x4a\x1b\x10\xae\x4b\x08\x00\x2b\x34\x9a\x02\x00\x00": "ole32.dll",
"\xd0\x3f\x14\x88\x8d\xc2\x2b\x4b\x8f\xef\x8d\x88\x2f\x6a\x93\x90\x01\x00": "lsm.exe",
"\xe6\x73\x0c\xe6\xf9\x88\xcf\x11\x9a\xf1\x00\x20\xaf\x6e\x72\xf4\x02\x00": "rpcss.dll",
"\x6c\xfc\x79\xde\x6f\xdc\xc7\x43\xa4\x8e\x63\xbb\xc8\xd4\x00\x9d\x01\x00": "rdpclip.exe",
"\x41\x82\xb5\x68\x59\xc2\x03\x4f\xa2\xe5\xa2\x65\x1d\xcb\xc9\x30\x01\x00": "cryptsvc.dll",
"\x80\xa9\x88\x10\xe5\xea\xd0\x11\x8d\x9b\x00\xa0\x24\x53\xc3\x37\x01\x00": "mqqm.dll",
"\xcf\x0b\xa7\x7e\xaf\x48\x6a\x4f\x89\x68\x6a\x44\x07\x54\xd5\xfa\x01\x00": "nsisvc.dll",
"\xe0\xca\x02\xec\xe0\xb9\xd2\x11\xbe\x62\x00\x20\xaf\xed\xdf\x63\x01\x00": "mq1repl.dll",
"\xb3\x8b\x0b\x59\xf6\x4e\xa4\x4c\x83\xcf\xbe\x06\xc4\x07\x86\x74\x01\x00": "PSIService.exe",
"\xce\x9f\x75\x89\x25\x5a\x86\x40\x89\x67\xde\x12\xf3\x9a\x60\xb5\x01\x00": "tssdjet.dll",
"\x5d\x2c\x95\x25\x76\x79\xa1\x4a\xa3\xcb\xc3\x5f\x7a\xe7\x9d\x1b\x01\x00": "wlansvc.dll",
"\xc5\x41\x19\xdf\x89\xfe\x79\x4e\xbf\x10\x46\x36\x57\xac\xf4\x4d\x01\x00": "efssvc.dll",
"\xc1\xcd\x1a\x8f\x4d\x75\xeb\x43\x96\x29\xaa\x16\x20\x92\x8e\x65\x00\x00": "IMEPADSM.DLL",
"\xdf\x76\x49\x65\x98\x14\x56\x40\xa1\x5e\xcb\x4e\x87\x58\x4b\xd8\x01\x00": "emdmgmt.dll",
"\xe0\x42\xc7\x4f\x10\x4a\xcf\x11\x82\x73\x00\xaa\x00\x4a\xe6\x73\x03\x00": "dfssvc.exe",
"\xfa\xdb\x6e\x0b\x24\x4a\xc6\x4f\x8a\x23\x94\x2b\x1e\xca\x65\xd1\x01\x00": "spoolsv.exe",
"\xc8\xb7\xd4\x12\xd5\x77\xd1\x11\x8c\x24\x00\xc0\x4f\xa3\x08\x0d\x01\x00": "lserver.dll",
"\x44\xaf\x7d\x8c\xdc\xb6\xd1\x11\x9a\x4c\x00\x20\xaf\x6e\x7c\x57\x01\x00": "appmgmts.dll",
"\xae\x99\x86\x9b\x44\x0e\xb1\x47\x8e\x7f\x86\xa4\x61\xd7\xec\xdc\x00\x00": "rpcss.dll",
"\x84\x65\x0a\x0b\x0f\x9e\xcf\x11\xa3\xcf\x00\x80\x5f\x68\xcb\x1b\x01\x01": "rpcss.dll",
"\xa2\x9c\x14\x93\x3b\x97\xd1\x11\x8c\x39\x00\xc0\x4f\xb9\x84\xf9\x00\x00": "scecli.dll",
"\x7d\x25\x13\xfc\x67\x55\xea\x4d\x89\x8d\xc6\xf9\xc4\x84\x15\xa0\x01\x00": "mqqm.dll",
"\x82\x26\xb9\x2f\x99\x65\xdc\x42\xae\x13\xbd\x2c\xa8\x9b\xd1\x1c\x01\x00": "MPSSVC.dll",
"\x76\x22\x3a\x33\x00\x00\x00\x00\x0d\x00\x00\x80\x9c\x00\x00\x00\x03\x00": "rpcrt4.dll",
"\xf0\x0e\xd7\xd6\x3b\x0e\xcb\x11\xac\xc3\x08\x00\x2b\x1d\x29\xc4\x01\x00": "locator.exe",
"\xdd\x34\x91\x1a\x39\x7b\xba\x45\xad\x88\x44\xd0\x1c\xa4\x7f\x28\x01\x00": "mqqm.dll",
"\xfe\x95\x31\x9b\x03\xd6\xd1\x43\xa0\xd5\x90\x72\xd7\xcd\xe1\x22\x01\x00": "tssdjet.dll",
"\x55\x1a\x20\x6f\x4d\xa2\x5f\x49\xaa\xc9\x2f\x4f\xce\x34\xdf\x98\x01\x00": "iphlpsvc.dll",
"\x5f\x2e\x7e\x89\xf3\x93\x76\x43\x9c\x9c\xfd\x22\x77\x49\x5c\x27\x01\x00": "dfsrmig.exe",
"\x90\x2c\xfe\x98\x42\xa5\xd0\x11\xa4\xef\x00\xa0\xc9\x06\x29\x10\x01\x00": "advapi32.dll",
"\x0c\xc5\xad\x30\xbc\x5c\xce\x46\x9a\x0e\x91\x91\x47\x89\xe2\x3c\x01\x00": "nrpsrv.dll",
"\x1e\x24\x2f\x41\x2a\xc1\xce\x11\xab\xff\x00\x20\xaf\x6e\x7a\x17\x00\x02": "rpcss.dll",
"\xe6\x53\x3a\x9f\xb1\xcb\x54\x4e\x87\x8e\xaf\x9f\x82\x3a\xa3\xf1\x01\x00": "MpRtMon.dll",
"\xa8\xe5\xfc\x1d\x8a\xdd\x33\x4e\xaa\xce\xf6\x03\x92\x2f\xd9\xe7\x00\x01": "wpcsvc.dll",
"\xf0\x0e\xd7\xd6\x3b\x0e\xcb\x11\xac\xc3\x08\x00\x2b\x1d\x29\xc3\x01\x00": "locator.exe",
"\x46\xd7\xd0\xe3\xaf\xd2\xfd\x40\x8a\x7a\x0d\x70\x78\xbb\x70\x92\x01\x00": "qmgr.dll",
"\x5a\x23\xb5\xc6\x13\xe4\x1d\x48\x9a\xc8\x31\x68\x1b\x1f\xaa\xf5\x01\x01": "SCardSvr.dll",
"\x5a\x23\xb5\xc6\x13\xe4\x1d\x48\x9a\xc8\x31\x68\x1b\x1f\xaa\xf5\x01\x00": "SCardSvr.dll",
"\x69\x45\x81\x7d\xb3\x35\x50\x48\xbb\x32\x83\x03\x5f\xce\xbf\x6e\x01\x00": "ias.dll",
"\x41\xea\x25\x48\xe3\x51\x2a\x4c\x84\x06\x8f\x2d\x26\x98\x39\x5f\x01\x00": "userenv.dll",
"\xc4\xfe\xfc\x99\x60\x52\x1b\x10\xbb\xcb\x00\xaa\x00\x21\x34\x7a\x00\x00": "rpcss.dll",
"\xc5\x28\x47\x3c\xab\xf0\x8b\x44\xbd\xa1\x6c\xe0\x1e\xb0\xa6\xd5\x01\x00": "dhcpcsvc.dll",
"\xe0\x8e\x20\x41\x70\xe9\xd1\x11\x9b\x9e\x00\xe0\x2c\x06\x4c\x39\x01\x00": "mqqm.dll",
"\xbf\x7b\x40\xcb\x4f\xc1\xd9\x4c\x8f\x55\xcb\xb0\x81\x46\x59\x8c\x00\x00": "IMJPDCT.EXE",
"\x78\x56\x34\x12\x34\x12\xcd\xab\xef\x00\x01\x23\x45\x67\xcf\xfb\x01\x00": "netlogon.dll",
"\x30\x4c\xda\x83\x3a\xea\xcf\x11\x9c\xc1\x08\x00\x36\x01\xe5\x06\x01\x00": "nfsclnt.exe",
"\x1f\xa7\x37\x21\x5e\xbb\x29\x4e\x8e\x7e\x2e\x46\xa6\x68\x1d\xbf\x09\x00": "wspsrv.exe - Microsoft ISA Server",
"\x1e\x67\xe9\xc0\xc6\x33\x38\x44\x94\x64\x56\xb2\xe1\xb1\xc7\xb4\x01\x00": "wbiosrvc.dll",
"\x80\xbd\xa8\xaf\x8a\x7d\xc9\x11\xbe\xf4\x08\x00\x2b\x10\x29\x89\x01\x00": "rpcrt4.dll",
"\x8b\x3c\xf1\x6a\x44\x08\x83\x4c\x90\x64\x18\x92\xba\x82\x55\x27\x01\x00": "tssdis.exe",
"\x55\x51\xd8\xec\x3a\xcc\x10\x4f\xaa\xd5\x9a\x9a\x2b\xf2\xef\x0c\x01\x00": "termsrv.dll",
"\xe8\x98\x8b\xbb\xdd\x84\xe7\x45\x9f\x34\xc3\xfb\x61\x55\xee\xed\x01\x00": "vaultsvc.dll",
"\x86\xb1\x49\xd0\x4f\x81\xd1\x11\x9a\x3c\x00\xc0\x4f\xc9\xb2\x32\x01\x00": "ntfrs.exe",
"\x5d\x2c\x95\x25\x76\x79\xa1\x4a\xa3\xcb\xc3\x5f\x7a\xe7\x9d\x1b\x01\x01": "wlansvc.dll",
"\x7f\x0b\xfe\x64\xf5\x9e\x53\x45\xa7\xdb\x9a\x19\x75\x77\x75\x54\x01\x00": "rpcss.dll",
"\x86\xd4\xdc\x68\x9e\x66\xd1\x11\xab\x0c\x00\xc0\x4f\xc2\xdc\xd2\x02\x00": "ismserv.exe",
"\xc3\x26\xf2\x76\x14\xec\x25\x43\x8a\x99\x6a\x46\x34\x84\x18\xae\x01\x00": "winlogon.exe",
"\x23\x05\x7a\xfd\x70\xdc\xdd\x43\x9b\x2e\x9c\x5e\xd4\x82\x25\xb1\x01\x00": "appinfo.dll",
"\x40\xfd\x2c\x34\x6c\x3c\xce\x11\xa8\x93\x08\x00\x2b\x2e\x9c\x6d\x00\x00": "llssrv.exe",
"\x84\xd8\xb6\x8f\x88\x23\xd0\x11\x8c\x35\x00\xc0\x4f\xda\x27\x95\x04\x01": "w32time.dll",
"\x9b\x06\x33\xae\xa8\xa2\xee\x46\xa2\x35\xdd\xfd\x33\x9b\xe2\x81\x01\x00": "spoolsv.exe",
"\x26\xb5\x55\x1d\x37\xc1\xc5\x46\xab\x79\x63\x8f\x2a\x68\xe8\x69\x01\x00": "rpcss.dll",
"\xa0\xaa\x17\x6e\x47\x1a\xd1\x11\x98\xbd\x00\x00\xf8\x75\x29\x2e\x02\x00": "clussvc.exe",
"\xdf\x5f\xe9\xbd\xe0\xee\xde\x45\x9e\x12\xe5\xa6\x1c\xd0\xd4\xfe\x01\x00": "termsrv.dll",
"\xac\xbe\x00\xc1\x3a\xd3\x4b\x4a\xbf\x23\xbb\xef\x46\x63\xd0\x17\x01\x00": "wcncsvc.dll",
"\x78\x56\x34\x12\x34\x12\xcd\xab\xef\x00\x01\x23\x45\x67\x89\xab\x01\x00": "spoolsv.exe",
"\x06\x50\x7b\x8a\x13\xcc\xdb\x11\x97\x05\x00\x50\x56\xc0\x00\x08\x01\x00": "appidsvc.dll",
"\x20\x60\xae\x91\x3c\x9e\xcf\x11\x8d\x7c\x00\xaa\x00\xc0\x91\xbe\x00\x00": "certsrv.exe",
"\x16\xbb\x74\x81\x1b\x57\x38\x4c\x83\x86\x11\x02\xb4\x49\x04\x4a\x01\x00": "p2psvc.dll",
"\x36\x00\x61\x20\x22\xfa\xcf\x11\x98\x23\x00\xa0\xc9\x11\xe5\xdf\x01\x00": "rasmans.dll",
"\x70\x0d\xec\xec\x03\xa6\xd0\x11\x96\xb1\x00\xa0\xc9\x1e\xce\x30\x01\x00": "ntdsbsrv.dll",
"\x1c\xef\x74\x0a\xa4\x41\x06\x4e\x83\xae\xdc\x74\xfb\x1c\xdd\x53\x01\x00": "schedsvc.dll",
"\x25\x04\x49\xdd\x25\x53\x65\x45\xb7\x74\x7e\x27\xd6\xc0\x9c\x24\x01\x00": "BFE.DLL",
"\x7c\x5a\xcc\xf5\x64\x42\x1a\x10\x8c\x59\x08\x00\x2b\x2f\x84\x26\x15\x00": "ntdsa.dll",
"\xa0\x01\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x46\x00\x00": "rpcss.dll",
"\x49\x59\xd3\x86\xc9\x83\x44\x40\xb4\x24\xdb\x36\x32\x31\xfd\x0c\x01\x00": "schedsvc.dll",
"\x35\x08\x22\x11\x26\x5b\x94\x4d\xae\x86\xc3\xe4\x75\xa8\x09\xde\x01\x00": "lsasrv.dll",
"\xa8\x66\x00\xc8\x79\x75\xfc\x44\xb9\xb2\x84\x66\x93\x07\x91\xb0\x01\x00": "umrdp.dll",
"\xab\x59\xec\xf1\xa9\x4c\x30\x4c\xb2\xd0\x54\xef\x1d\xb4\x41\xb7\x01\x00": "iertutil.dll",
"\xba\xaa\x67\x52\x49\x4f\x53\x46\x8e\x26\xd1\xe1\x1f\x3f\x2a\xd9\x01\x00": "termsrv.dll",
"\x60\x9e\xe7\xb9\x52\x3d\xce\x11\xaa\xa1\x00\x00\x69\x01\x29\x3f\x00\x00": "rpcss.dll",
"\x60\x9e\xe7\xb9\x52\x3d\xce\x11\xaa\xa1\x00\x00\x69\x01\x29\x3f\x00\x02": "rpcss.dll",
"\x38\x47\xaf\x3f\x21\x3a\x07\x43\xb4\x6c\xfd\xda\x9b\xb8\xc0\xd5\x01\x02": "audiosrv.dll",
"\x38\x47\xaf\x3f\x21\x3a\x07\x43\xb4\x6c\xfd\xda\x9b\xb8\xc0\xd5\x01\x01": "audiosrv.dll",
"\x20\x32\x5f\x2f\x26\xc1\x76\x10\xb5\x49\x07\x4d\x07\x86\x19\xda\x01\x02": "netdde.exe",
"\xbf\x11\x9d\x7f\xb9\x7f\x6b\x43\xa8\x12\xb2\xd5\x0c\x5d\x4c\x03\x01\x00": "MPSSVC.dll",
"\xbf\x52\x5a\xb2\xdd\xe5\x4a\x4f\xae\xa6\x8c\xa7\x27\x2a\x0e\x86\x01\x00": "keyiso.dll",
"\x04\x22\x11\x4b\x19\x0e\xd3\x11\xb4\x2b\x00\x00\xf8\x1f\xeb\x9f\x01\x00": "ssdpsrv.dll",
"\x97\xb2\xee\x04\xf4\xcb\x6b\x46\x8a\x2a\xbf\xd6\xa2\xf1\x0b\xba\x01\x00": "efssvc.dll",
"\x40\xb2\x9b\x20\x19\xb9\xd1\x11\xbb\xb6\x00\x80\xc7\x5e\x4e\xc1\x01\x00": "irmon.dll",
"\x96\x3f\xf0\x76\xfd\xcd\xfc\x44\xa2\x2c\x64\x95\x0a\x00\x12\x09\x01\x00": "spoolsv.exe",
"\x4a\xa5\xbb\x06\x05\xbe\xf9\x49\xb0\xa0\x30\xf7\x90\x26\x10\x23\x01\x00": "wscsvc.dll",
"\xa6\xb2\xdd\x1b\xc3\xc0\xbe\x41\x87\x03\xdd\xbd\xf4\xf0\xe8\x0a\x01\x00": "dot3svc.dll",
"\x82\x15\x41\xaa\xdf\x9b\xfb\x48\xb4\x2b\xfa\xa1\xee\xe3\x39\x49\x01\x00": "nlasvc.dll",
"\xfa\x9d\xd7\xd2\x00\x34\xd0\x11\xb4\x0b\x00\xaa\x00\x5f\xf5\x86\x01\x00": "dmadmin.exe",
"\x12\xfc\x99\x60\xff\x3e\xd0\x11\xab\xd0\x00\xc0\x4f\xd9\x1a\x4e\x03\x00": "FXSAPI.dll",
"\x1e\x24\x2f\x41\x2a\xc1\xce\x11\xab\xff\x00\x20\xaf\x6e\x7a\x17\x00\x00": "rpcss.dll",
"\xd5\x33\x9a\x2c\xdb\xf1\x2d\x47\x84\x64\x42\xb8\xb0\xc7\x6c\x38\x01\x00": "tbssvc.dll",
"\x30\x7c\xde\x3d\x5d\x16\xd1\x11\xab\x8f\x00\x80\x5f\x14\xdb\x40\x01\x00": "services.exe",
"\x86\xb1\x49\xd0\x4f\x81\xd1\x11\x9a\x3c\x00\xc0\x4f\xc9\xb2\x32\x01\x01": "ntfrs.exe",
"\x94\x8c\x95\x95\x24\xa4\x55\x40\xb6\x2b\xb7\xf4\xd5\xc4\x77\x70\x01\x00": "winlogon.exe",
"\xe3\x31\x67\x32\xc0\xc1\x69\x4a\xae\x20\x7d\x90\x44\xa4\xea\x5c\x01\x00": "profsvc.dll",
"\x18\x5a\xcc\xf5\x64\x42\x1a\x10\x8c\x59\x08\x00\x2b\x2f\x84\x26\x38\x00": "ntdsai.dll",
"\x0f\x6a\xe9\x4b\x52\x9f\x29\x47\xa5\x1d\xc7\x06\x10\xf1\x18\xb0\x01\x00": "wbiosrvc.dll",
"\x80\x42\xad\x82\x6b\x03\xcf\x11\x97\x2c\x00\xaa\x00\x68\x87\xb0\x02\x00": "infocomm.dll",
"\x87\x04\x26\x1f\x29\xba\x13\x4f\x92\x8a\xbb\xd2\x97\x61\xb0\x83\x01\x00": "termsrv.dll",
"\x70\x07\xf7\x18\x64\x8e\xcf\x11\x9a\xf1\x00\x20\xaf\x6e\x72\xf4\x00\x00": "ole32.dll",
"\xc0\xeb\x4f\xfa\x91\x45\xce\x11\x95\xe5\x00\xaa\x00\x51\xe5\x10\x04\x00": "autmgr32.exe",
"\x10\xca\x8c\x70\x69\x95\xd1\x11\xb2\xa5\x00\x60\x97\x7d\x81\x18\x01\x00": "mqdssrv.dll",
"\x28\x2c\xf5\x45\x9f\x7f\x1a\x10\xb5\x2b\x08\x00\x2b\x2e\xfa\xbe\x01\x00": "WINS.EXE",
"\x31\xa3\x59\x2f\x7d\xbf\xcb\x48\x9e\x5c\x7c\x09\x0d\x76\xe8\xb8\x01\x00": "termsrv.dll",
"\x61\x26\x45\x4a\x90\x82\x36\x4b\x8f\xbe\x7f\x40\x93\xa9\x49\x78\x01\x00": "spoolsv.exe",
}

def uuid_to_exe(_uuid):
    if KNOWN_UUIDS.has_key(_uuid):
        return KNOWN_UUIDS[_uuid]
    else:
        return 'unknown'

#Protocol ids, reference: http://www.opengroup.org/onlinepubs/9629399/apdxi.htm

class NDRFloor:
    PROTO_ID = { 0x0: 'OSI OID',
                 0x2: 'UUID',
                 0x5: 'OSI TP4',
                 0x6: 'OSI CLNS or DNA Routing',
                 0x7: 'DOD TCP',
                 0x8: 'DOD UDP',
                 0x9: 'DOD IP',
                 0xa: 'RPC connectionless protocol',
                 0xb: 'RPC connection-oriented protocol',
                 0xd: 'UUID',
                 0x2: 'DNA Session Control',
                 0x3: 'DNA Session Control V3',
                 0x4: 'DNA NSP Transport',
                 0x0d: 'Netware SPX', 
                 0x0e: 'Netware IPX', #someone read hexa as decimal? (0xe=0x14 in opengroup's list)
                 # [MS-RPCE] RPC over SMB MUST use a protocol identifier of 0x0F instead of 0x10, 
                 # as specified in [C706] Appendix I.
                 0x0f: 'Named Pipes',
                 0x10: 'Named Pipes',
                 0x11: 'NetBIOS',
                 # [MS-RPCE] RPC over NetBIOS over TCP MUST use a protocol identifier of 0x12 instead
                 # of the value 0x11, as specified in [C706] Appendix I.
                 0x12: 'NetBIOS',
                 0x13: 'Netware SPX',
                 0x14: 'Netware IPX',
                 0x16: 'Appletalk Stream',
                 0x17: 'Appletalk Datagram',
                 0x18: 'Appletalk',
                 0x19: 'NetBIOS extra',
                 0x1a: 'Vines SPP',
                 0x1b: 'Vines IPC',
                 0x1c: 'StreeTalk',
                 0x20: 'Unix Domain Socket',
                 0x21: 'null',
                 0x22: 'NetBIOS extra'}
                 
    def __init__(self,data=''):
        self._lhs_len = 0
        self._protocol = 0
        self._uuid = ''
        self._rhs_len = 0
        self._rhs = ''
        self._floor_len = 0
        if data:
            self._lhs_len, self._protocol = unpack('<HB',data[:3])
            offset = 3
            if self._protocol == 0x0d: # UUID
                self._uuid = data[offset:offset+self._lhs_len-1]
                offset += self._lhs_len-1
            self._rhs_len = unpack('<H',data[offset:offset+2])[0]
            offset += 2
            self._rhs = data[offset:offset+self._rhs_len]
            self._floor_len = offset + self._rhs_len
                                               
    def get_floor_len(self):
        return self._floor_len
    def get_protocol(self):
        return self._protocol
    def get_rhs(self):
        return self._rhs
    def get_rhs_len(self):
        return self._rhs_len
    def get_uuid(self):
        return self._uuid
    def get_protocol_string(self):
        if NDRFloor.PROTO_ID.has_key(self._protocol):
            return NDRFloor.PROTO_ID[self._protocol]
        else:
            return 'unknown'
    def get_uuid_string(self):
        if len(self._uuid) == 18:
            version = unpack('<H',self._uuid[16:18])[0]
            return "%s version: %d" % (parse_uuid(self._uuid), version)
        else:
            return ''

ID_PROTO = dict((v,k) for k, v in NDRFloor.PROTO_ID.iteritems())

def parse_uuid(_uuid):
    return uuid.bin_to_string(_uuid)

class NDRTower:
    def __init__(self,data=''):
        self._length = 0
        self._length2 = 0
        self._number_of_floors = 0
        self._floors = []
        self._tower_len = 0
        if data:
            self._length, self._length2, self._number_of_floors = unpack('<LLH',data[:10])
            offset = 10
            for i in range(0,self._number_of_floors):
                self._floors.append(NDRFloor(data[offset:]))
                offset += self._floors[i].get_floor_len()
            self._tower_len = offset
    def get_tower_len(self):
        return self._tower_len
    def get_floors(self):
        return self._floors
    def get_number_of_floors(self):
        return self._number_of_floors
    
                                    
class NDREntry:
    def __init__(self,data=''):
        self._objectid = ''
        self._entry_len = 0
        self._tower = 0
        self._referent_id = 0
        self._annotation_offset = 0
        self._annotation_len = 0
        self._annotation = ''
        if data:
            self._objectid = data[:16]
            self._referent_id = unpack('<L',data[16:20])[0]
            self._annotation_offset, self._annotation_len = unpack('<LL',data[20:28])
            self._annotation = data[28:28+self._annotation_len-1]
            if self._annotation_len % 4:
                self._annotation_len += 4 - (self._annotation_len % 4)
            offset = 28 + self._annotation_len
            self._tower = NDRTower(data[offset:])
            self._entry_len = offset + self._tower.get_tower_len()
    def get_entry_len(self):
        if self._entry_len % 4:
            self._entry_len += 4 - (self._entry_len % 4)
        return self._entry_len
    def get_annotation(self):
        return self._annotation
    def get_tower(self):
        return self._tower

    def get_uuid(self):
        binuuid = self._tower.get_floors()[0].get_uuid()
        return binuuid[:16]

    def get_objuuid(self):
        return self._objectid

    def get_version(self):
        binuuid = self._tower.get_floors()[0].get_uuid()
        return unpack('<H', binuuid[16:18])[0]

    def print_friendly(self):
        if self._tower <> 0:
            floors = self._tower.get_floors()
            print "IfId: %s [%s]" % (floors[0].get_uuid_string(), uuid_to_exe(floors[0].get_uuid()))
            if self._annotation:
                print "Annotation: %s" % self._annotation
            print "UUID: %s" % parse_uuid(self._objectid)
            print "Binding: %s" % self.get_string_binding()
            print ''

    def get_string_binding(self):
        if self._tower <> 0:
            tmp_address = ''
            tmp_address2 = ''
            floors = self._tower.get_floors()
            num_floors = self._tower.get_number_of_floors()
            for i in range(3,num_floors):
                if floors[i].get_protocol() == 0x07:
                    tmp_address = 'ncacn_ip_tcp:%%s[%d]' % unpack('!H',floors[i].get_rhs())
                elif floors[i].get_protocol() == 0x08:
                    tmp_address = 'ncadg_ip_udp:%%s[%d]' % unpack('!H',floors[i].get_rhs())
                elif floors[i].get_protocol() == 0x09:
                    # If the address were 0.0.0.0 it would have to be replaced by the remote host's IP.
                    tmp_address2 = socket.inet_ntoa(floors[i].get_rhs())
                    if tmp_address <> '':
                        return tmp_address % tmp_address2
                    else:
                        return 'IP: %s' % tmp_address2
                elif floors[i].get_protocol() == 0x0c:
                    tmp_address = 'ncacn_spx:~%%s[%d]' % unpack('!H',floors[i].get_rhs())
                elif floors[i].get_protocol() == 0x0d:
                    n = floors[i].get_rhs_len()
                    tmp_address2 = ('%02X' * n) % unpack("%dB" % n, floors[i].get_rhs())
                    if tmp_address <> '':
                        return tmp_address % tmp_address2
                    else:
                        return 'SPX: %s' % tmp_address2
                elif floors[i].get_protocol() == 0x0e:
                    tmp_address = 'ncadg_ipx:~%%s[%d]' % unpack('!H',floors[i].get_rhs())
                elif floors[i].get_protocol() == 0x0f:
                    tmp_address = 'ncacn_np:%%s[%s]' % floors[i].get_rhs()[:floors[i].get_rhs_len()-1]
                elif floors[i].get_protocol() == 0x10:
                    return 'ncalrpc:[%s]' % floors[i].get_rhs()[:floors[i].get_rhs_len()-1]
                elif floors[i].get_protocol() == 0x01 or floors[i].get_protocol() == 0x11:
                    if tmp_address <> '':
                        return tmp_address % floors[i].get_rhs()[:floors[i].get_rhs_len()-1]
                    else:
                        return 'NetBIOS: %s' % floors[i].get_rhs()
                elif floors[i].get_protocol() == 0x1f:
                    tmp_address = 'ncacn_http:%%s[%d]' % unpack('!H',floors[i].get_rhs())
                else:
                    if floors[i].get_protocol_string() == 'unknown':
                        return 'unknown_proto_0x%x:[0]' % floors[i].get_protocol()
                    elif floors[i].get_protocol_string() <> 'UUID':
                        return 'protocol: %s, value: %s' % (floors[i].get_protocol_string(), floors[i].get_rhs())


class NDREntries:
    def __init__(self,data=''):
        self._max_count = 0
        self._offset = 0
        self._actual_count = 0
        self._entries_len = 0
        self._entries = []
        if data:
            self._max_count, self._offset, self._actual_count = unpack('<LLL',data[:12])
            self._entries_len = 12
            for i in range (0,self._actual_count):
                self._entries.append(NDREntry(data[self._entries_len:]))
                self._entries_len += self._entries[i].get_entry_len()
                
    def get_max_count(self):
        return self._max_count
    def get_offset(self):
        return self._offset
    def get_actual_count(self):
        return self._actual_count
    def get_entries_len(self):
        return self._entries_len
    def get_entry(self):
        return self._entries[0]
    
class NDRPointer:
    def __init__(self,data='',pointerType = None):
        self._referent_id = random.randint(1,65535)
        self._pointer = None
        if data:
            self._referent_id = unpack('<L',data[:4])[0]
            self._pointer = pointerType(data[4:])
    def set_pointer(self, data):
        self._pointer = data
    def get_pointer(self):
        return self._pointer
    def rawData(self):
        return pack('<L',self._referent_id) + self._pointer.rawData()

class NDRString:
    def __init__(self,data=''):
        self._string = ''
        self._max_len = 0
        self._offset = 0
        self._length = 0
        if data:
            self._max_len, self._offset, self._length = unpack('<LLL',data[:12])
            self._string = unicode(data[12:12 + self._length * 2], 'utf-16le')
    def get_string(self):
        return self._string
    def set_string(self,str):
        self._string = str
        self._max_len = self._length = len(str)+1
    def rawData(self):
        if self._length & 0x1:
            self._tail = pack('<HH',0,0)
        else:
            self._tail = pack('<H',0)
        return pack('<LLL',self._max_len, self._offset, self._length) + self._string.encode('utf-16le') + self._tail

    def get_max_len(self):
        return self._max_len

    def get_length(self):
        return self._length
    
class NDRStringA(Structure):
    structure = (
        ('MaxCount','<L=len(Data)'),
        ('Offset','<L=0'),
        ('ActualCount','<L=len(Data)'),
        ('DataLen','_-Data','MaxCount'),
        ('Data',':'),
    )

class NDRPointerNew(Structure):
    structure = (
        ('RefId','<L=0xff'),
    )
    def __init__(self, data = None, alignment = 0):
        Structure.__init__(self,data, alignment)
        self['RefId'] = random.randint(1,65535)

class NDRUniqueStringA(NDRStringA):
    commonHdr = (
        ('RefId','<L'),
    )
    def __init__(self, data = None, alignment = 0):
        NDRStringA.__init__(self,data, alignment)
        self['RefId'] = random.randint(1,65535)


class NDRStringW(Structure):
    alignment = 4
    structure = (
        ('MaxCount','<L=len(Data)/2'),
        ('Offset','<L=0'),
        ('ActualCount','<L=len(Data)/2'),
        ('DataLen','_-Data','MaxCount*2'),
        ('Data',':'),
    )

class NDRUniqueStringW(NDRStringW):
    alignment = 4
    commonHdr = (
        ('RefId','<L'),
    )
    def __init__(self, data = None, alignment = 0):
        NDRStringW.__init__(self,data, alignment)
        self['RefId'] = random.randint(1,65535)


class pRPC_UNICODE_STRING(Structure):
    # Pointer to a RPC_UNICODE_STRING
    structure = (
        ('Length','<H=0'),
        ('MaximumLength','<H=0'),
        ('NDRStringPtr','<L=0'),
    )

    def __init__(self, data = None, alignment = 0):
        Structure.__init__(self, data, alignment)
        self['NDRStringPtr'] = random.randint(1,65535)

    def setDataLen(self, data):
        self['Length'] = len(data)
        self['MaximumLength'] = self['Length']

class RPC_UNICODE_STRING(Structure):
    # Same as NDRStringW except DataLen is taken from ActualCount
    structure = (
        ('MaxCount','<L=len(Data)/2'),
        ('Offset','<L=0'),
        ('ActualCount','<L=len(Data)/2'),
        ('DataLen','_-Data','ActualCount*2'),
        ('Data',':'),
    )

    def __init__(self, data = None, alignment = 0):
        Structure.__init__(self, data, alignment)

class NDRConformantVaryingArray(Structure):
    structure = (
        ('MaxCount','<L=len(Data)'),
        ('Offset','<L=0'),
        ('ActualCount','<L=len(Data)'),
        ('DataLen','_-Data','ActualCount'),
        ('Data',':'),
    )

