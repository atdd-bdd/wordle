from Words import *
from timer import Timer


def main():
    words = Words("words002.txt")
    words.read_words()
    print("Checking against words ")
    t = Timer()
    t.start()
    out = []
    index = 0
    print ("size of words", len(words.words))
    for word in words.words:
        # if 'A' in word and 'B' in word:
        out.append([word, index])
        index += 1
    print(" out length ", len(out))
    # print(out)

    print(" Time elapsed ", t.stop())
    t2 = Timer()
    t2.start()
    position_count = CountAndPosition(words.words)
    print("Time to count all words ", t2.stop())
    print("Count per position", position_count.positions)
    print("totals by char ", position_count.totals)
    t3 = Timer()
    t3.start()
    out = []
    for word in words.words:
        score = position_count.score_on_totals(word)
        out.append([word, score])
    print(" Time to score all words ", t3.stop())


if __name__ == "__main__":
    main()
