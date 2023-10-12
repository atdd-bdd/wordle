from CountAndPosition import CountAndPosition


def main():
    test_list = [[3, 'b'], [5, 'a'], [4, 'c']]
    out_dict = {}
    for item in test_list:
        out_dict[item[1]] = item[0]
    out_dict['f'] = 7
    out_dict['e'] = 6
    for item in enumerate(out_dict.keys()):
        print("value is ", item)
        print("value is ", item[0], item[1])
        print("value is ", out_dict[item[1]])
    test_list.sort(reverse=True)
    print(test_list)
    for item in test_list:
        out_dict[item[0]] = item[1]

    words = ['ABCDE', 'FGHIJ', 'ABCIJ', "EDCBA", "VWXYJ", "VWXDA"]
    print(words)
    positions = CountAndPosition(words)
    for word in words:
        position_score = positions.score_on_position_counts(word)
        total_score = positions.score_on_totals(word)
        print("Word ", word, " Total ", total_score, " position ", position_score)

    max_position_score = 0
    max_words_position = []
    for word in max_words:
        position_score = positions.score_on_position_counts(word)
        print("word ", word, " position score ", position_score)
        if position_score == max_position_score:
            max_words_position.append(word)
        if position_score > max_position_score:
            max_words_position = [word]
            max_position_score = position_score
    print(max_words_position)




if __name__ == "__main__":
    main()
