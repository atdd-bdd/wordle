import unittest
from GamePlayer import *
from Words import filter_guesses_by_highest_char_occurrence, filter_guesses_by_position_in_word

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
        self.assertEqual(words.count_and_position.totals, {'A': 3, 'B': 0, 'C': 2, 'D': 1, 'E': 4, 'F': 0,
                                                           'G': 0,
                                                           'H': 1,
                                                           'I': 0, 'J': 0, 'K': 3, 'L': 0, 'M': 0, 'N': 2,
                                                           'O': 2,
                                                           'P': 0,
                                                           'Q': 0, 'R': 5, 'S': 1, 'T': 2, 'U': 1, 'V': 1,
                                                           'W': 7,
                                                           'X': 0,
                                                           'Y': 0, 'Z': 0})

    def test_filter_guesses_by_highest_char_occurrence(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        current_words = words.words
        current_words = filter_guesses_by_highest_char_occurrence(current_words, must_chars,
                                                                  words.count_and_position)
        self.assertEqual(current_words, ['WREAK', 'WREST'])

    def test_filter_guesses_by_position_in_word(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        current_words = ['WREAK', 'WRECK', 'WREST']
        must_chars = ''
        current_words = filter_guesses_by_position_in_word(current_words, must_chars, words.count_and_position)
        self.assertEqual(current_words, ['WRECK'])

    def test_create_guess(self):
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
        guesses = words.create_guess(must_chars, words.count_and_position)
        Trace.write(list_to_str(guesses))
        self.assertEqual(guesses, ['WREST'])

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
        # words = ["FOCAL", "LOCAL", "STATE", "STEAK", "TEASE", "VOCAL", "YEAST", "LEAST", "STAVE", "TRUSS",
        # "TRUST",
        #          "CRUST", "SWEAT", "POUND", "PRIZE", "SHAVE", "SHARE", "SNARE", "SPARE", "TAUNT", "JAUNT",
        #          "HAUNT",
        #          "GAUNT", "VAUNT", "WATCH", "WIGHT", "WINCH", "WOUND", "GRAZE", "SNAIL"]
        # t = Timer()
        word_map = {'FOCAL': 4, 'LOCAL': 4, 'STATE': 4, 'STEAK': 4, 'TEASE': 4, 'VOCAL': 4, 'YEAST': 4, 'LEAST': 3,
                    'STAVE': 3, 'TRUSS': 3, 'TRUST': 3, 'CRUST': 3, 'SWEAT': 3, 'POUND': 5, 'PRIZE': 4, 'SHAVE': 4,
                    'SHARE': 4, 'SNARE': 3, 'SPARE': 4, 'TAUNT': 4, 'JAUNT': 4, 'HAUNT': 3, 'GAUNT': 4, 'VAUNT': 5,
                    'WATCH': 5, 'WIGHT': 6, 'WINCH': 4, 'WOUND': 5, 'GRAZE': 5, 'SNAIL': 3, 'SKUNK': 4, 'STEER': 4,
                    'ESTER': 3, 'RESET': 4}

        new_map = {}
        for index, word in enumerate(word_map):
            current_turns = word_map[word]
            print(" word ", word, " turns ", current_turns)
            t = Timer()
            t.start()
            turns = test_game(word, game, server)
            print("Word ", word, " turns ", turns, " current turns ", current_turns)
            new_map[word] = turns
            if turns != current_turns:
                print("** Better or worse ? ")
            self.assertLess(turns, 7, " For word " + word)
            print(t.stop())
        #print(new_map)
        Log.close()
        Trace.close()


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
    Trace.write(" *-- Test Game ")
    server.answer = word
    Log.write("Answer=" + server.answer)
    Trace.write("Answer=" + server.answer)
    turns = run_a_game(game, server)
    Trace.write("Turns " + str(turns))
    Trace.write("---End test game ")
    return turns


if __name__ == '__main__':
    unittest.main()
