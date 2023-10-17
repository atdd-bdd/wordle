from Words import *
from timer import Timer


def main():
    words = Words("words002.txt")
    words.read_words()
    print("Checking against words ")
    t = Timer()
    t.start()
    out = []
    print ("size of words", len(words.words))
    for word in words.words:
        # if 'A' in word and 'B' in word:
        out.append(word)
    print(" out length ", len(out))
    print(out)

    print(" Time elapsed ", t.stop())
    a=5.3445345
    b = f"{a: .2f}"
    print(b)


if __name__ == "__main__":
    main()
