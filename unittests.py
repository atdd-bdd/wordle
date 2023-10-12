import unittest
from GamePlayer import *
from Words import filter_guesses_by_highest_char_occurance, filter_guesses_by_position_in_word

from timer import Timer


# noinspection SpellCheckingInspection
class MyTestCase(unittest.TestCase):

    def test_word_read(self):
        words = words_for_testing()
        self.assertEqual(words.count(), 7)
        self.assertEqual(words.words, ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST'])

    def test_make_filter_no_guesses(self):
        guesses = []
        matches = []
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        self.assertEqual(must_chars, "")
        self.assertEqual(not_chars, "")
        self.assertEqual(not_here_chars, ['', '', '', '', ''])
        self.assertEqual(position_chars, ['', '', '', '', ''])

    def test_make_filter_one_guess(self):
        guesses = []
        matches = []
        guesses.append("WOVEN")
        matches.append("ENNYN")
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        self.assertEqual(must_chars, 'WE')
        self.assertEqual(not_chars, 'OVN')
        self.assertEqual(not_here_chars, ['', '', '', 'E', ''])
        self.assertEqual(position_chars, ['W', '', '', '', ''])

    def test_make_filter_two_guesses(self):
        guesses = []
        matches = []
        guesses.append("WOVEN")
        matches.append("ENNYN")
        guesses.append("WRENC")
        matches.append("EEENY")
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        self.assertEqual(must_chars, 'WERC')
        self.assertEqual(not_chars, 'OVN')
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
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        filtered = words.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars)
        self.assertEqual(filtered.words, ['WRACK', 'WRECK'])

    def test_count_chars_and_sort(self):
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']

        words.count_chars()
        self.assertEqual(words.char_counts_total, {'A': 3, 'B': 0, 'C': 2, 'D': 1, 'E': 4, 'F': 0, 'G': 0, 'H': 1,
                                                   'I': 0, 'J': 0, 'K': 3, 'L': 0, 'M': 0, 'N': 2, 'O': 2, 'P': 0,
                                                   'Q': 0, 'R': 5, 'S': 1, 'T': 2, 'U': 1, 'V': 1, 'W': 7, 'X': 0,
                                                   'Y': 0, 'Z': 0})
        sorted_char_counts_in_position = words.sort_char_counts_in_position()
        self.assertEqual(sorted_char_counts_in_position, [['A', 2], ['B', 0], ['C', 3], ['D', 4], ['E', 2], ['F', 0],
                                                          ['G', 0], ['H', 4], ['I', 0], ['J', 0], ['K', 4], ['L', 0],
                                                          ['M', 0], ['N', 3], ['O', 1], ['P', 0], ['Q', 0], ['R', 1],
                                                          ['S', 3], ['T', 3], ['U', 2], ['V', 2], ['W', 0], ['X', 0],
                                                          ['Y', 0], ['Z', 0]])
        sorted_values = words.sorted_count_chars()

        self.assertEqual(sorted_values, ['W', 'R', 'E', 'A', 'K', 'C', 'N', 'O', 'T', 'D', 'H', 'S', 'U', 'V'])

    def test_filter_guesses_by_highest_char_occurrence(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        sorted_values = words.sorted_count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        current_words = words.words
        current_words = filter_guesses_by_highest_char_occurance(current_words, must_chars, sorted_values)
        self.assertEqual(current_words, ['WREAK'])

    def test_filter_guesses_by_position_in_word(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        sorted_values = words.sorted_count_chars()
        current_words = ['WREAK', 'WRECK', 'WREST']
        current_words = filter_guesses_by_position_in_word(current_words, words.sort_char_counts_in_position(),
                                                           sorted_values)
        self.assertEqual(current_words, ['WRECK'])

    def test_create_guess(self):
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        sorted_values = words.sorted_count_chars()
        sorted_char_counts_in_position = words.sort_char_counts_in_position()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        guess = words.create_guess(sorted_values, must_chars, sorted_char_counts_in_position)
        Trace.write(guess)
        self.assertEqual(guess, 'WREAK')

    def test_server(self):
        answers_filename = "test_answers.txt"
        data_filename = "test_words.txt"
        server = Server(data_filename, answers_filename)
        server.set_answer(1)
        Trace.write("Answer is " + server.answer)
        self.assertEqual(server.answer, "WOUND")
        result = server.check_guess("WORSE")
        self.assertEqual(result, 'WORSE EENNN')

        result = server.check_guess("WOUND")
        self.assertEqual(result, 'WOUND EEEEE')

    def test_games(self):
        game, server = setup_game()
        Trace()
        Log()
        Trace.write("Doing test games ")
        words = ["FOCAL", "LOCAL", "STATE", "STEAK", "TEASE", "VOCAL", "YEAST", "LEAST", "STAVE", "TRUSS", "TRUST",
                 "CRUST", "SWEAT", "POUND", "PRIZE", "SHAVE", "SHARE", "SNARE", "SPARE", "TAUNT", "JAUNT", "HAUNT",
                 "GAUNT", "VAUNT", "WATCH", "WIGHT", "WINCH", "WOUND", "GRAZE", "SNAIL"]
        t = Timer()
        map = {'FOCAL': 3, 'LOCAL': 4, 'STATE': 4, 'STEAK': 3, 'TEASE': 4, 'VOCAL': 5, 'YEAST': 5, 'LEAST': 3,
               'STAVE': 3,
               'TRUSS': 3, 'TRUST': 3, 'CRUST': 3, 'SWEAT': 4, 'POUND': 6, 'PRIZE': 4, 'SHAVE': 5, 'SHARE': 3,
               'SNARE': 4,
               'SPARE': 5, 'TAUNT': 6, 'JAUNT': 5, 'HAUNT': 5, 'GAUNT': 5, 'VAUNT': 5, 'WATCH': 6, 'WIGHT': 6,
               'WINCH': 6,
               'WOUND': 6, 'GRAZE': 5, 'SNAIL': 4}
        for index, word in enumerate(map):
            current_turns = map[word]
            print(" word ", word, " turns ", current_turns)
            t.start()
            turns = test_game(word, game, server)
            print("Word ", word, " turns ", turns, " current turns ", current_turns)
            if turns != current_turns:
                print("** Better or worse ? ")
            self.assertLess(turns, 7, " For word " + word)
            print(t.stop())
        Log.close()
        Trace.close()

    def setUp(self):
        pass


def setup_game():
    data_filename = "words002.txt"
    answers_filename = "answers.txt"
    game = GameRound(data_filename, answers_filename)
    server = Server(data_filename, answers_filename)
    return game, server


def words_for_testing():
    data_filename = "test_answers.txt"
    words = Words(data_filename)
    words.read_words()
    return words


def test_game(word, game, server):
    Trace.write(" **** Test Game *****")
    server.answer = word
    Log.write("Answer " + server.answer)
    Trace.write("Answer " + server.answer)
    turns = run_a_game(game, server)
    Trace.write("Turns " + str(turns))
    Trace.write("*** End test game ****")
    return turns


if __name__ == '__main__':
    unittest.main()
