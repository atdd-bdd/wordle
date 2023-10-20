import re

from utilities import list_to_str_with_quotes


def filter_values_to_string(must_chars, not_chars, not_here_chars, position_chars, repeated_chars):
    s = "Must chars {" + must_chars + "} "
    s += "Not chars {" + not_chars + "} "
    s += "Not here chars " + list_to_str_with_quotes(not_here_chars) + " "
    s += "Position chars " + list_to_str_with_quotes(position_chars)
    s += "Repeated chars {" + repeated_chars + "} "
    return s


def filter_list(word_list, position_chars, must_chars, not_chars, not_here_chars, repeated_chars):
    new_word_list = []
    for word in word_list:
        skip = False
        for i in range(len(word)):
            c = word[i]
            skip = has_not_here_char(c, i, not_here_chars, skip)
            if skip:
                break
            skip = does_not_have_position_chars(c, i, position_chars, skip)
            if skip:
                break
            skip = has_not_char(c, not_chars, skip)
            if skip:
                break
        if skip:
            continue
        skip = has_all_must_chars(must_chars, skip, word)
        if not skip:
            new_word_list.append(word)
    return new_word_list


def has_not_char(c, not_chars, skip):
    for d in not_chars:
        if c == d:
            skip = True
    return skip


def does_not_have_position_chars(c, i, position_chars, skip):
    if position_chars[i] != "":
        if c != position_chars[i]:
            skip = True
    return skip


def has_not_here_char(c, i, not_here_chars, skip):
    for d in not_here_chars[i]:
        if c == d:
            skip = True
            break
    return skip


def has_all_must_chars(must_chars, skip, word):
    for c in must_chars:
        has_char = False
        for i in range(len(word)):
            if word[i] == c:
                has_char = True
                break
        if not has_char:
            skip = True
            break
    return skip


def determine_repeated_chars(guess, match, repeated_chars):
    value_IN_WORD_MATCH = 'Y'
    value_EXACT_MATCH = 'E'
    chars = {}
    for i in range(len(guess)):
        c = guess[i]
        if match[i] == value_EXACT_MATCH or match[i] == value_IN_WORD_MATCH:
            if chars.get(c) is None:
                chars[c] = 1
            else:
                chars[c] += 1
    print (" values are ", chars)
    for key in chars.keys():
        count = chars[key]
        if count > 1:
            repeated_chars = add_to_string(key, repeated_chars)
    return repeated_chars



def make_filter_values(guesses, matches):
    value_NO_MATCH = 'N'
    value_IN_WORD_MATCH = 'Y'
    value_EXACT_MATCH = 'E'
    not_chars = ""
    must_chars = ""
    repeated_chars = ''
    position_chars = ["", "", "", "", ""]
    not_here_chars = ["", "", "", "", ""]
    number_guesses = len(guesses)
    for j in range(number_guesses):
        guess_size = len(guesses[0])
        guess = guesses[j]
        match = matches[j]
        for i in range(guess_size):
            g = guess[i]
            m = match[i]

            if m == value_NO_MATCH:
                not_chars = add_to_string(g, not_chars)
                not_here_chars[i] = add_to_string(g, not_here_chars[i])
            if m == value_IN_WORD_MATCH:
                must_chars = add_to_string(g, must_chars)
                not_here_chars[i] = add_to_string(g, not_here_chars[i])
            if m == value_EXACT_MATCH:
                position_chars[i] = g
                must_chars = add_to_string(g, must_chars)
        repeated_chars = determine_repeated_chars(guess, match, repeated_chars)
    # if guess word had repeated characters, but one of them was marked yes.
    for c in must_chars:
        not_chars = not_chars.replace(c, "")

    return must_chars, not_chars, not_here_chars, position_chars, repeated_chars


def add_to_string(g, not_chars):
    match = re.search(g, not_chars)
    if match is None:
        not_chars += g
    return not_chars


def score_on_not_here_counts(word, not_here_chars, positions):
    i = 0
    score = 0
    for c in word:
        char_score = positions[c][i]
        # Trace.write("char  " + c + " at index " + str(i) +
        #             " has char score" + str(char_score) + " not here " +
        #             not_here_chars[i])
        if char_score == 0:
            char_score = 1
        if c in not_here_chars[i]:
            score -= char_score
        i = i + 1
    # Trace.write(" Not here score " + word + " " + str(score))

    return score
