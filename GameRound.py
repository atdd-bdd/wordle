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
        t1 = Timer()
        t1.start()
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered = self.answers.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars)
        # Trace.write("Time to filter " + str(t1.stop()))
        #Log.write("Filtered count " + str(filtered.count()))
        Trace.write("Filtered words " + list_to_str(filtered.words))
        if filtered.count() <= 2:
            Trace.write("Selecting from one or two words " + str(filtered.count()))
            return filtered.first_word()
        t2 = Timer()
        t2.start()
        filtered.count_chars()
        guesses = self.all_words.create_guess(must_chars,not_here_chars,filtered.count_and_position )
        # Trace.write("Time to create guess - all words " + str(t2.stop()) )
        if len(guesses) >= 1:
            return guesses[0]
        Trace.write("@@@No guesses from create guess - now use the words themselves. ")
        t3 = Timer()
        t3.start()
        filtered.count_chars()
        # No more information from guess list,  uses the filtered answers
        not_here_chars = ["", "", "", "", ""]
        guesses = filtered.create_guess("", not_here_chars, filtered.count_and_position)
        Trace.write("Time to create guess from filtered " + str(t3.stop()))
        if len(guesses) >= 1:
            return guesses[0]
        return "ZZZZZ"

