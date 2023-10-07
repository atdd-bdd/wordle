import unittest
from Words import *
from GameRound import *
from filter import *
from server import *

class MyTestCase(unittest.TestCase):

    def test_word_read(self):
        words = self.Words_for_testing()
        self.assertEqual(words.count(), 7)
        self.assertEqual(words.words, ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST'])

    def test_make_filter_no_guesses(self):
        guesses = []
        matches = []
        must_chars, not_chars, not_here_chars, position_chars =  make_filter_values(guesses, matches)
        self.assertEqual(must_chars, "")
        self.assertEqual(not_chars, "")
        self.assertEqual(not_here_chars, ['', '', '', '', ''])
        self.assertEqual(position_chars, ['', '', '', '', ''])

    def test_make_filter_one_guess(self):
        guesses = []
        matches = []
        guesses.append("WOVEN")
        matches.append("ENNYN")
        must_chars, not_chars, not_here_chars, position_chars =  make_filter_values(guesses, matches)
        self.assertEqual(must_chars, 'WE')
        self.assertEqual(not_chars,'OVN')
        self.assertEqual(not_here_chars, ['', '', '', 'E', ''])
        self.assertEqual(position_chars, ['W', '', '', '', ''])

    def test_make_filter_two_guesses(self):
        guesses = []
        matches = []
        guesses.append("WOVEN")
        matches.append("ENNYN")
        guesses.append("WRENC")
        matches.append("EEENY")
        must_chars, not_chars, not_here_chars, position_chars =  make_filter_values(guesses, matches)
        self.assertEqual(must_chars, 'WERC')
        self.assertEqual(not_chars,'OVN')
        self.assertEqual(not_here_chars, ['', '', '', 'E', 'C'])
        self.assertEqual(position_chars, ['W', 'R', 'E', '', ''])


    def test_filter_list(self):
        word_list = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered_words = filter_list(word_list, position_chars, must_chars, not_chars, not_here_chars)
        self.assertEqual(filtered_words, ['WRACK', 'WRECK'])

    def test_create_filtered_list(self):
        words = self.Words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses =[ "WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered= words.create_filtered_words( position_chars, must_chars, not_chars, not_here_chars)
        self.assertEqual(filtered.words, ['WRACK', 'WRECK'])

    def Words_for_testing(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.read_words()
        return words

    def test_count_chars_and_sort(self):
        words = self.Words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']

        words.count_chars()
        self.assertEqual(words.char_counts_total, {'A': 3, 'B': 0, 'C': 2, 'D': 1, 'E': 4, 'F': 0, 'G': 0, 'H': 1,
                                                   'I': 0, 'J': 0, 'K': 3, 'L': 0, 'M': 0, 'N': 2, 'O': 2, 'P': 0,
                                                   'Q': 0, 'R': 5, 'S': 1, 'T': 2, 'U': 1, 'V': 1, 'W': 7, 'X': 0,
                                                   'Y': 0, 'Z': 0})
        sorted_char_counts_in_position =  words.sort_char_counts_in_position()
        self.assertEqual(sorted_char_counts_in_position, [['A', 2], ['B', 0], ['C', 3], ['D', 4], ['E', 2], ['F', 0],
                                                          ['G', 0], ['H', 4], ['I', 0], ['J', 0], ['K', 4], ['L', 0],
                                                          ['M', 0], ['N', 3], ['O', 1], ['P', 0], ['Q', 0], ['R', 1],
                                                          ['S', 3], ['T', 3], ['U', 2], ['V', 2], ['W', 0], ['X', 0],
                                                          ['Y', 0], ['Z', 0]])
        sorted_values = words.sorted_count_chars()

        self.assertEqual(sorted_values, ['W', 'R', 'E', 'A', 'K', 'C', 'N', 'O', 'T', 'D', 'H', 'S', 'U', 'V', 'B',
                                         'F', 'G', 'I', 'J', 'L', 'M', 'P', 'Q', 'X', 'Y', 'Z'])

    def test_filter_guesses_by_highest_char_occurrence(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words =  ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        sorted_values = words.sorted_count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        current_words = words.words
        current_words = words.filter_guesses_by_highest_char_occurance(current_words, must_chars, sorted_values)
        self.assertEqual(current_words,  ['WREAK', 'WRECK', 'WREST'])

    def test_filter_guesses_by_position_in_word(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        sorted_values = words.sorted_count_chars()
        current_words = ['WREAK', 'WRECK', 'WREST']
        current_words = words.filter_guesses_by_position_in_word(current_words,words.sort_char_counts_in_position(), sorted_values)
        self.assertEqual(current_words,['WRECK'] )

    def test_create_guess(self):
        words = self.Words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        sorted_values = words.sorted_count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        guess = words.create_guess(sorted_values, must_chars)
        print(guess)
        self.assertEqual(guess, ['WRECK'])

    def test_server(self):
        answers_filename = "test_answers.txt"
        data_filename = "test_words.txt"
        server = Server(data_filename, answers_filename)
        server.set_answer(1)
        print("Answer is ", server.answer)
        self.assertEqual(server.answer,"WOUND")
        result = server.check_guess("WORSE")
        self.assertEqual(result,'WORSE EENNN')

        result = server.check_guess("WOUND")
        self.assertEqual(result, 'WOUND EEEEE')

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
