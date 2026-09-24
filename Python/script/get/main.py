import time
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from setting import PASSWORD, USERNAME, INIT_URL
from script.decrypt import md5, random, sha1, xbase
from script.get.get_netloc import get_netloc
from script.get.get_onlineip import get_onlineip
import requests
import json


def get_challenge_resp(netloc,headers,ip,timestamp,callback,username=USERNAME):
    params={
    "callback":callback,
    "ip":ip ,
    "_":timestamp,
    "username":username
    }
    resp=requests.get(url=f"{netloc}/cgi-bin/get_challenge",headers=headers,params=params)
    raw_resp=resp.text.split("(")[1][:-1]
    json_resp=json.loads(raw_resp)
    token=json_resp["challenge"]
    return token

def link_to_net(netloc,token,timestamp,ip,callback,headers,username=USERNAME,password=PASSWORD):
    info={"username":username,"password":password,"ip":ip ,"acid":"21","enc_ver":"srun_bx1"}
    i=xbase.build_srbx1(info, token)
    hmd5=md5.md5encode(password=password,token=token)

    s=token+username
    s+=token+hmd5
    s+=token+"21"
    s+=token+ip 
    s += token + "200"
    s += token + "1"
    s += token + i

    chksum=sha1.sha1encode(s)
    p={
    "callback":callback,
    "action": 'login',
    "username": username,
    "password":'{MD5}' + hmd5,
    "os": "Windows 10",
    "name": "Windows",
    "double_stack": "0",
    "chksum": chksum,
    "info": i,
    "ac_id": "21",
    "ip": ip ,
    "n": "200",
    "type": "1",
    "_":timestamp
    }

    resp=requests.get(url=f"{netloc}/cgi-bin/srun_portal",headers=headers,params=p)

    return resp.text

if __name__=="__main__":
    netloc=get_netloc(INIT_URL)
    headers={
        "Referer":f"{netloc}/srun_portal_pc?ac_id=21&theme=pro",
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0",
        "Accept":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-encoding":"gzip, deflate"
    }
    ip=get_onlineip(init_url=INIT_URL,headers=headers)
    timestamp=str(int(time.time() * 1000))
    callback=random.simulate("1.12.4",True,ts=timestamp)

    token=get_challenge_resp(netloc=netloc,headers=headers,ip=ip,timestamp=timestamp,callback=callback,username=USERNAME)
    resp_txt=link_to_net(netloc=netloc,token=token,timestamp=timestamp,ip=ip,callback=callback,headers=headers,username=USERNAME,password=PASSWORD)
    print(repr(resp_txt))