from Words import *


class GameRound:
    def __init__(self, all_words_filename, answers_filename):
        self.all_words = Words(all_words_filename)
        self.all_words.read_words()
        print(" Length of ", all_words_filename, " ", self.all_words.count())
        self.all_words.count_chars()
        self.all_words.sorted_count_chars()
        self.answers = Words(answers_filename)
        self.answers.read_words()
        print(" Length of ", answers_filename, " ", self.answers.count())
        self.answers.count_chars()
        self.answers.sorted_count_chars()

    def get_guess(self, guesses, matches):
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered = self.answers.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars)
        filtered.count_chars()
        if filtered.count() <= 2:
            return filtered.first_word()
        sorted_values = filtered.sorted_count_chars()
        guess = self.all_words.create_guess(sorted_values, must_chars)
        return guess
