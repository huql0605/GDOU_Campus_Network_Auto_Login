import re
import random
def js_math_random():
    """模拟 JavaScript 的 Math.random()，返回 [0, 1) 之间的浮点数"""
    return random.random()

def simulate(m, m_is_string=False, ts=""):

    
    if m_is_string:
        # 对应 JS 中：m + Math.random() 且 m 是字符串 → 字符串拼接
        s = str(m) + str(random.random())
    else:
        # 对应 JS 中：m + Math.random() 且 m 是数字 → 数值相加
        s = str(m + random.random())
    
    # 对应 .replace(/\D/g, "")：删除所有非数字字符
    digits = re.sub(r'\D', '', s)
    return "jQuery" + digits+"_"+ts