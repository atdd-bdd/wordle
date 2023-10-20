def list_to_str(a_list):
    maxy = len(a_list)
    if maxy > 50:
        maxy = 50
    out = "[" + str(len(a_list)) + "] "
    for index in range(maxy):
        out += ' ' + str(a_list[index])
    return out


def list_to_str_with_quotes(a_list):
    maxy = len(a_list)
    if maxy > 50:
        maxy = 50
    out = "[" + str(len(a_list)) + "] "
    for index in range(maxy):
        out += ' "' + a_list[index] + '" '
    return out


def list_list_to_str(a_list):
    maxy = len(a_list)
    if maxy > 50:
        maxy = 50
    out = "[" + str(len(a_list)) + "] "
    for index in range(maxy):
        out += ' ' + str(a_list[index][0]) + '=' + str(a_list[index][1])
    return out


def sort_function(e):
    return e[1]


def check_repeats(word):
    chars = {}
    for c in word:
        if chars.get(c) is None:
            chars[c] = 1
        else:
            chars[c] += 1
    out = ""
    for key in chars.keys():
        count = chars[key]
        if count > 1:
            out += key
    return out
