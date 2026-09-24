import json
import math

# ---------- UTF-16 码元转换（兼容 JS charCodeAt） ----------
def to_utf16_units(s):
    units = []
    for ch in s:
        code = ord(ch)
        if code <= 0xFFFF:
            units.append(code)
        else:
            code -= 0x10000
            high = 0xD800 + (code >> 10)
            low = 0xDC00 + (code & 0x3FF)
            units.append(high)
            units.append(low)
    return units

# ---------- s 函数：字符串 → 32 位整数数组 ----------
def s(a, b):
    units = to_utf16_units(a)
    c = len(units)
    v = []
    for i in range(0, c, 4):
        code0 = units[i] if i < c else 0
        code1 = units[i+1] if i+1 < c else 0
        code2 = units[i+2] if i+2 < c else 0
        code3 = units[i+3] if i+3 < c else 0
        val = (code0 | (code1 << 8) | (code2 << 16) | (code3 << 24)) & 0xFFFFFFFF
        v.append(val)
    if b:
        v.append(c)
    return v

# ---------- l 函数：32 位整数数组 → 二进制字符串 ----------
def l(a, b):
    d = len(a)
    c = (d - 1) << 2
    if b:
        m = a[-1]
        if m < c - 3 or m > c:
            return None
        c = m
    chars = []
    for v in a:
        v = v & 0xFFFFFFFF
        chars.append(chr(v & 0xFF))
        chars.append(chr((v >> 8) & 0xFF))
        chars.append(chr((v >> 16) & 0xFF))
        chars.append(chr((v >> 24) & 0xFF))
    s = ''.join(chars)
    return s[:c] if b else s

# ---------- XXTEA 变种加密 ----------
def encode(str_data, key):
    if str_data == '':
        return ''
    v = s(str_data, True)
    k = s(key, False)
    if len(k) < 4:
        k += [0] * (4 - len(k))
    n = len(v) - 1
    z = v[n]
    y = v[0]
    c = 0x9E3779B9  # 0x86014019 | 0x183639A0
    q = math.floor(6 + 52 / (n + 1))
    d = 0
    while q > 0:
        q -= 1
        d = (d + c) & 0xFFFFFFFF
        e = (d >> 2) & 3
        for p in range(n):
            y = v[p + 1]
            m = ((z >> 5) ^ (y << 2)) & 0xFFFFFFFF
            m = (m + (((y >> 3) ^ (z << 4) ^ (d ^ y)) & 0xFFFFFFFF)) & 0xFFFFFFFF
            m = (m + ((k[(p & 3) ^ e] ^ z) & 0xFFFFFFFF)) & 0xFFFFFFFF
            v[p] = (v[p] + m) & 0xFFFFFFFF
            z = v[p]
        p = n
        y = v[0]
        m = ((z >> 5) ^ (y << 2)) & 0xFFFFFFFF
        m = (m + (((y >> 3) ^ (z << 4) ^ (d ^ y)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        m = (m + ((k[(p & 3) ^ e] ^ z) & 0xFFFFFFFF)) & 0xFFFFFFFF
        v[n] = (v[n] + m) & 0xFFFFFFFF
        z = v[n]
    return l(v, False)

# ---------- 自定义 Base64 编码 ----------
def custom_base64_encode(data_str, alpha):
    data = bytes(ord(ch) & 0xFF for ch in data_str)
    result = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        while len(chunk) < 3:
            chunk += b'\x00'
        b0, b1, b2 = chunk[0], chunk[1], chunk[2]
        n = (b0 << 16) | (b1 << 8) | b2
        c0 = (n >> 18) & 0x3F
        c1 = (n >> 12) & 0x3F
        c2 = (n >> 6) & 0x3F
        c3 = n & 0x3F
        result.append(alpha[c0])
        result.append(alpha[c1])
        if i + 1 < len(data):
            result.append(alpha[c2])
        else:
            result.append('=')
        if i + 2 < len(data):
            result.append(alpha[c3])
        else:
            result.append('=')
    return ''.join(result)

# ---------- 主函数：生成 {SRBX1}... ----------
def build_srbx1(info_dict, token):
    # 注意：键顺序需与 JS 中对象字面量一致
    info_str = json.dumps(info_dict, separators=(',', ':'), ensure_ascii=False)
    encrypted = encode(info_str, token)
    alpha = 'LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA'
    b64_str = custom_base64_encode(encrypted, alpha)
    return '{SRBX1}' + b64_str

