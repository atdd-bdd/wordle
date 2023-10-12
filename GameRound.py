from Words import *
from Log import *
from Words import filter_guesses_by_highest_char_occurrence
from timer import Timer

class GameRound:
    def __init__(self, all_words_filename, answers_filename):
        self.all_words = Words(all_words_filename)
        self.all_words.read_words()
        Trace.write("Length of " + all_words_filename + " " + str(self.all_words.count()))
        self.all_words.count_chars()
        self.answers = Words(answers_filename)
        self.answers.read_words()
        Trace.write("Length of " + answers_filename + " " + str(self.answers.count()))
        self.answers.count_chars()

    def get_guess(self, guesses, matches):

        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered = self.answers.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars)

        Log.write("Filtered count " + str(filtered.count()))
        Trace.write("Filtered words " + list_to_str(filtered.words))
        if filtered.count() <= 2:
            Trace.write("Selecting from two words")
            return filtered.first_word()
        filtered.count_chars()
        guesses = self.all_words.create_guess(must_chars,filtered.count_and_position )
        if len(guesses) >= 1:
            return guesses[0]
        Trace.write("@@@No guesses from create guess - now use the words themselves. ")
        filtered.count_chars()
        # No more information from guess list,  uses the filtered answers
        guesses = filtered.create_guess("", filtered.count_and_position)
        if len(guesses) >= 1:
            return guesses[0]
        return "ZZZZZ"

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
        count_and_position = CountAndPosition(current_words)
        ret = filter_guesses_by_highest_char_occurrence(current_words, must_chars, count_and_position)
        Trace.write("Ret is " + list_to_str(ret))
        return ret[0]
