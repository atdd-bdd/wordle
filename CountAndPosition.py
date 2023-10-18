from Log import Trace
from timer import Timer


class CountAndPosition:
    def __init__(self, words):
        t1 = Timer()
        t1.start()
        self.positions = {}
        for c in "ABCDEFGHIJKLMNOPQRSTURVWXYZ":
            self.positions[c] = [0, 0, 0, 0, 0]

        for word in words:
            i = 0
            for c in word:
                self.positions[c][i] += 1
                i += 1
        # print(self.positions)
        self.totals = {}
        for position in enumerate(self.positions.keys()):
            char = position[1]
            counts = self.positions[char]
            # print("char ", char, "  count ", counts)
            total = 0

            for i in range(5):
                total += counts[i]
            self.totals[char] = total
        Trace.write("Setting up counts " + t1.stop())
        # print("totals ", self.totals)

    def zero_in_totals(self, char_seq):
        # print("Deleting from total ", char_seq)

        for c in char_seq:
            self.totals[c] = 0
            self.positions[c] = [0, 0, 0, 0, 0]

    def score_on_totals(self, word):
        score = 0
        scored_already = ""
        for c in word:
            if c in scored_already:
                continue
            scored_already += c
            char_score = self.totals.get(c, -1)
            if char_score == -1:
                print("***Did not find char in score on totals", c)
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
