def sanitize_string(input_string):
    # 将字符串中的 NUL 字符替换为其他字符（这里使用空格）
    sanitized_string = input_string.replace('\x00', ' ')
    return sanitized_string


def isfloat(value):
    try:
        float_value = float(value)
        return True
    except ValueError:
        return False