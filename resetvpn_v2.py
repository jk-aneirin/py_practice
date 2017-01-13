#!/usr/bin/env python
import json
import os,sys
import random
import subprocess
import time
import logging

logging.basicConfig(level= logging.DEBUG,\
        format = '%(asctime)s %(levelname)s %(message)s',\
        datefmt = '%a, %d %b %Y %H:%M:%S',\
        filename = '/path/sockproxy.log',\
        filemode = 'a+')

class ResetProxy():
    def __init__(self):
        self.confile='/etc/shadowsocks/config.json'
        self.proxy=""

    def GetOneProxy(self):
        s1=["a.bad.com","b.bad.com","c.bad.com"]
        s2=["d.aa.com","e.aa.com"]
        s3=["f.bb.com","g.bb.com"]
        s1.extend(s2)
        s1.extend(s3)
        while True:
            self.proxy=random.choice(s1)
            if self.Iseq(self.proxy):
                continue
            else:
                return

    def Iseq(self,s):
        with open(self.confile,'r') as json_file:
            ct=json.load(json_file)
            origserver=ct['server']
        if s==origserver:
            return True
        else:
            return False

    def Mdfconf(self):
        self.GetOneProxy()
        with open(self.confile) as json_file:
            ct=json.load(json_file)
            ct['server']=self.proxy
        self.Store(ct)
        self.Rst()

    def Store(self,data):
        with open(self.confile,'w') as json_file:
            json_file.write(json.dumps(data))

    def Rst(self):
        os.system('service sslocal restart')

def LinkStatus():
    httpcode=subprocess.Popen('curl -s -o /dev/null -I -w "%{http_code}" -x socks5h://10.0.2.33:7070 https://www.facebook.com',\
                            shell=True,stdout=subprocess.PIPE)
    if httpcode.stdout.read()=='200':
        return True
    else:
        return False

if __name__=="__main__":
    if LinkStatus():
        sys.exit(0)
    else:
        time.sleep(10)
        if not LinkStatus():
            rp=ResetProxy()
            rp.Mdfconf()
            logging.warning('Change Proxy Server {}'.format(rp.proxy))
        else:
            sys.exit(0)

