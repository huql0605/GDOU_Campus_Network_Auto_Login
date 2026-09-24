import hmac, hashlib
def md5encode(password:str,token:str):
    
    hmd5 = hmac.new(
        token.encode('utf-8'),
        password.encode('utf-8'),
        hashlib.md5
    ).hexdigest()
    return hmd5