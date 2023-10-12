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
    positions = PositionInWord(words)
    for word in words:
        position_score = positions.score_on_position_counts(word)
        total_score = positions.score_on_totals(word)
        print("Word ", word, " Total ", total_score, " position ", position_score)

    max_total_score = 0
    max_words = []
    for word in words:
        total_score = positions.score_on_totals(word)
        print("Word ", word, " Total ", total_score)
        if total_score == max_total_score:
            max_words.append(word)
        if total_score > max_total_score:
            max_words = [word]
            max_total_score = total_score

    print(max_words)
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


class PositionInWord:
    def __init__(self, words):
        self.positions = {}
        for c in "ABCDEFGHIJKLMNOPQRSTURVWXYZ":
            self.positions[c] = [0, 0, 0, 0, 0]

        for word in words:
            i = 0
            for c in word:
                self.positions[c][i] += 1
                i += 1
        print(self.positions)
        self.totals = {}
        for position in enumerate(self.positions.keys()):
            char = position[1]
            counts = self.positions[char]
            # print("char ", char, "  count ", counts)
            total = 0

            for i in range(5):
                total += counts[i]
            self.totals[char] = total
        print("totals ", self.totals)

    def delete_from_totals(self, char_seq):
        for c in char_seq:
            del self.totals[c]

    def score_on_totals(self, word):
        score = 0
        for c in word:
            char_score = self.totals[c]
            score += char_score
        return score

    def score_on_position_counts(self, word):
        i = 0
        score = 0
        for c in word:
            char_score = self.positions[c][i]
            score += char_score
            i = i + 1
        return score


if __name__ == "__main__":
    main()
