from Words import *
from Log import *
from Words import filter_guesses_by_highest_char_occurance


class GameRound:
    def __init__(self, all_words_filename, answers_filename):
        self.all_words = Words(all_words_filename)
        self.all_words.read_words()
        Trace.write("Length of " + all_words_filename + " " + str(self.all_words.count()))
        self.all_words.count_chars()
        self.all_words.sorted_count_chars()
        self.answers = Words(answers_filename)
        self.answers.read_words()
        Trace.write("Length of " + answers_filename + " " + str(self.answers.count()))
        self.answers.count_chars()
        self.answers.sorted_count_chars()

    def get_guess(self, guesses, matches):
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered = self.answers.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars)
        Log.write("Filtered count " + str(filtered.count()))
        Trace.write("Filtered words " + list_to_str(filtered.words))
        if len(must_chars) >= 5:
            Log.write("Have all must_chars " + must_chars)
            Trace.write("*** Have all the characters ***")
            return filtered.first_word()
        filtered.count_chars()
        if filtered.count() <= 2:
            Trace.write("Using just filtered words ")
            return filtered.first_word()
        if len(must_chars) == 4:
            return self.guess_with_four_known_chars(filtered, not_here_chars, position_chars, must_chars)
        sorted_values = filtered.sorted_count_chars()
        sorted_char_counts_in_position = filtered.sort_char_counts_in_position()
        guess = self.all_words.create_guess(sorted_values, must_chars, sorted_char_counts_in_position)
        return guess

    def guess_with_four_known_chars(self, filtered, not_here_chars, position_chars ,must_chars):
        Log.write("Have 4 must_chars ")
        ret, is_guess = filtered.create_guess_from_self(not_here_chars, position_chars, must_chars)
        if is_guess:
            Trace.write("Created guess from filtered")
            return ret
        else:
            return self.create_guess_from_chars_in_filtered(ret, must_chars)

    def create_guess_from_chars_in_filtered(self, ret, must_chars):
        Trace.write("Need to figure out words from " + ret)
        current_words = self.all_words.words
        sorted_values = []
        for c in ret:
            sorted_values.append(c)
        Trace.write("Sorted values are " + list_to_str(sorted_values))
        ret = filter_guesses_by_highest_char_occurance(current_words, must_chars, sorted_values)
        Trace.write("Ret is " + list_to_str(ret))
        return ret[0]
