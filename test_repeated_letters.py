from Words import *
from utilities import check_repeats


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
                print("** two repeated")


if __name__ == "__main__":
    main()
