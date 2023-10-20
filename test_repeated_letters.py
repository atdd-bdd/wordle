from Words import *
from timer import Timer


def check_repeats(word):
    chars = {}
    for c in word:
        if chars.get(c) is None:
            chars[c] = 1
        else:
            chars[c] += 1
        if chars[c] > 2:
            print("@@@@ triple")
    repeated = False
    out = ""
    for key in chars.keys():
        # print (key)
        count = chars[key]
        if count > 1:
            out += key
    return out



def main():
    Trace("trace_repeated_letters.txt ")

    words = Words("words002.txt")
    words.read_words()
    print("size of words", len(words.words))
    answers = Words("answers.txt")
    answers.read_words()
    print("size of answers", len(answers.words))
    count = 0
    for word in answers.words:
        # if count > 10:
        #     break
        count += 1
        repeated = check_repeats(word)
        if len(repeated) > 0:
            print(word, " has repeated ", repeated)
            if len(repeated) > 1:
                print ("** two repeated")




if __name__ == "__main__":
    main()
