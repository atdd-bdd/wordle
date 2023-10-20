from Log import Trace
from config import Configuration
from timer import Timer


class CountAndPosition:
    letters = "ABCDEFGHIJKLMNOPQRSTURVWXYZ"

    def __init__(self, words):
        t1 = Timer()
        t1.start()
        self.positions = {}

        for c in CountAndPosition.letters:
            self.positions[c] = [0, 0, 0, 0, 0]

        for word in words:
            i = 0
            for c in word:
                self.positions[c][i] += 1
                i += 1

        self.totals = {}
        for char, counts in self.positions.items():
            total = 0
            for i in range(5):
                total += counts[i]
            self.totals[char] = total
        # Trace.write("Setting up counts " + t1.stop())
        # print("totals ", self.totals)

        self.two_letters = {}
        for c in CountAndPosition.letters:
            for d in CountAndPosition.letters:
                self.two_letters[c + d] = 0

        for word in words:
            for i in range(len(word) - 1):
                pair = word[i] + word[i + 1]
                self.two_letters[pair] += 1

    def zero_in_totals(self, char_seq):
        # print("Deleting from total ", char_seq)

        for c in char_seq:
            self.totals[c] = 0
            self.positions[c] = [0, 0, 0, 0, 0]
            for d in CountAndPosition.letters:
                self.two_letters[c + d] = 0
                self.two_letters[d + c] = 0

    def alter_by_repeats(self, repeats):
        for c in repeats:
            self.totals[c] += Configuration.repeated_char_weighting

    def score_on_totals(self, word):
        score = 0
        scored_already = ""
        for c in word:
            if c in scored_already:
                continue
            scored_already += c
            char_score = self.totals.get(c, -1)
            if char_score == -1:
                Trace.write("@@@ Did not find char in score on totals: " + c)
                print("***Did not find char in score on totals", c)
                char_score = 0
            score += char_score
        return score

    def score_on_position_counts(self, word):
        i = 0
        score = 0
        for c in word:
            char_score = self.positions[c][i]
            score += char_score
            i = i + 1
        score = int(score * Configuration.position_score_weighting)
        return score

    def score_on_two_letters(self, word):
        score = 0
        for i in range(len(word) - 1):
            pair = word[i] + word[i + 1]
            char_score = self.two_letters.get(pair, -1)
            if char_score == -1:
                print("***Did not find pair in two letters:", pair)
                Trace.write("@@@ Did not find pair in two letters:" + pair)
                char_score = 0
            score += char_score
        score = int(score * Configuration.two_letter_score_weighting)
        return score
