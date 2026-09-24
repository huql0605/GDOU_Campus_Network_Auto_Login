import hashlib
def sha1encode(s:str):
    chksum=hashlib.sha1(s.encode("utf-8")).hexdigest()