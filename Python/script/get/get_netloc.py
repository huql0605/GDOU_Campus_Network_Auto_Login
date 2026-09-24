from urllib.parse import urlparse

def get_netloc(url:str):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"

