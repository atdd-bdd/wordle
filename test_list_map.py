from Words import *
from timer import Timer


def main():
    Trace("trace_list_map_timing")

    words = Words(Configuration.answer_filename)
    words.read_words()
    print("size of words", len(words.words))
    answers = Words(Configuration.answer_filename)
    answers.read_words()
    print("size of answers", len(answers.words))

    t = Timer()
    t.start()
    out = []
    index = 0
    for word in answers.words:
        out.append((word, index))
        index += 1
    print(" out length ", len(out))
    print(" Time to append words to new list ", t.stop())

    t = Timer()
    t.start()
    out = []
    index = 0
    for word in answers.words:
        out.append((word, index))
        index += 1
    print(" out length ", len(out))
    print(" Time to append words to new list with tuple ", t.stop())


    t2 = Timer()
    t2.start()
    position_count = CountAndPosition(answers.words)
    print("Time to count all answers ", t2.stop())

    # print("Count per position", position_count.positions)
    # print("totals by char ", position_count.totals)

    t3 = Timer()
    t3.start()
    out = []
    for word in words.words:
        score = position_count.score_on_totals(word)
        out.append((word, score))
    print(" Time to score all words ", t3.stop())

    t4 = Timer()
    t4.start()
    sorted_list = [(k, v) for k, v in position_count.totals.items()]
    print("Time to create with comprehension", t4.stop())
    sorted_list.sort(key=sort_function, reverse=True)
    print("Sorted positions ", sorted_list)

    t5 = Timer()
    t5.start()
    sorted_list1 = []
    for k, v in position_count.totals.items():
        sorted_list1.append((k, v))
    print("Time to create with loop ", t5.stop())
    sorted_list1.sort(key=sort_function, reverse=True)
    print("Sorted positions ", sorted_list1)


if __name__ == "__main__":
    main()
