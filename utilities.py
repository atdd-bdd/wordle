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
