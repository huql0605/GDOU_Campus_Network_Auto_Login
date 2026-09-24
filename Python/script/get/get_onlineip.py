import requests
from lxml import etree #type:ignore
import re
def get_onlineip(init_url:str,headers:dict):
    init_res=requests.get(init_url,headers)
    html = etree.HTML(init_res.text)
    script_text = html.xpath("//script[contains(text(), 'var CONFIG')]/text()")[0]
    m = re.search(r'\bip\s*:\s*"([^"]+)"', script_text)
    if m is None:
        raise ValueError("未能从页面脚本中提取 IP 地址")
    ip = m.group(1)
    return ip