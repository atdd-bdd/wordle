import unittest
from GamePlayer import *
from Words import filter_guesses_by_highest_char_occurrence, filter_guesses_by_position_in_word

from timer import Timer
from utilities import check_repeats


# noinspection SpellCheckingInspection
def test_position_and_count():
    word_list = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
    position_count = CountAndPosition(word_list)
    t1 = Timer()
    t1.start()
    for word in word_list:
        position_count.score_on_totals(word)
    print(" ***** Time to position count score ", t1.stop())


class MyTestCase(unittest.TestCase):

    def test_word_read(self):
        words = words_for_testing()
        self.assertEqual(7, words.count())
        self.assertEqual(['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST'], words.words)

    def test_determine_repeated_chars(self):
        guess = "AABBC"
        match = "EEYYN"
        repeated_chars = ""
        out = determine_repeated_chars(guess, match, repeated_chars)
        self.assertEqual("AB", out)

    def test_make_filter_no_guesses(self):
        guesses = []
        matches = []
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        self.assertEqual("", must_chars)
        self.assertEqual("", not_chars)
        self.assertEqual(['', '', '', '', ''], not_here_chars)
        self.assertEqual(['', '', '', '', ''], position_chars)
        self.assertEqual("", repeated_chars)

    def test_make_filter_one_guess(self):
        guesses = []
        matches = []
        guesses.append("WOVEN")
        matches.append("ENNYN")
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        self.assertEqual('WE', must_chars)
        self.assertEqual('OVN', not_chars)
        self.assertEqual(['', 'O', 'V', 'E', 'N'], not_here_chars)
        self.assertEqual(['W', '', '', '', ''], position_chars)
        self.assertEqual("", repeated_chars)

    def test_make_filter_with_repeated_guess(self):
        guesses = []
        matches = []
        guesses.append("ABCAB")
        matches.append("ENNYN")
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        self.assertEqual('A', must_chars)
        self.assertEqual('BC', not_chars)
        self.assertEqual(['', 'B', 'C', 'A', 'B'], not_here_chars)
        self.assertEqual(['A', '', '', '', ''], position_chars)
        self.assertEqual("A", repeated_chars)

    def test_make_filter_two_guesses(self):
        guesses = []
        matches = []
        guesses.append("WOVEN")
        matches.append("ENNYN")
        guesses.append("WRENC")
        matches.append("EEENY")
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        self.assertEqual('WERC', must_chars)
        self.assertEqual('OVN', not_chars)
        self.assertEqual(['', 'O', 'V', 'EN', 'NC'], not_here_chars)
        self.assertEqual(['W', 'R', 'E', '', ''], position_chars)
        self.assertEqual("", repeated_chars)

    def test_make_filter_three_guesses(self):
        guesses = []
        matches = []
        guesses.append("SOARE")
        matches.append("NENNN")
        guesses.append("CUNDY")
        matches.append("YNENN")
        guesses.append("IONIC")
        matches.append("NEEEE")
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        self.assertEqual('OCNI', must_chars)
        self.assertEqual('SAREUDY', not_chars)
        self.assertEqual(['SCI', 'U', 'A', 'RD', 'EY'], not_here_chars)
        self.assertEqual(['', 'O', 'N', 'I', 'C'], position_chars)
        self.assertEqual("", repeated_chars)

    def test_filter_list(self):
        word_list = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        filtered_words = filter_list(word_list, position_chars, must_chars, not_chars, not_here_chars, repeated_chars)
        self.assertEqual(['WRACK', 'WRECK'], filtered_words)

    def test_create_filtered_list(self):
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        filtered = words.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars, repeated_chars)
        self.assertEqual(['WRACK', 'WRECK'], filtered.words)

    def test_count_chars_and_sort(self):
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']

        words.count_chars()
        self.assertEqual({'A': 3, 'B': 0, 'C': 2, 'D': 1, 'E': 4, 'F': 0,
                          'G': 0,
                          'H': 1,
                          'I': 0, 'J': 0, 'K': 3, 'L': 0, 'M': 0, 'N': 2,
                          'O': 2,
                          'P': 0,
                          'Q': 0, 'R': 5, 'S': 1, 'T': 2, 'U': 1, 'V': 1,
                          'W': 7,
                          'X': 0,
                          'Y': 0, 'Z': 0}, words.count_and_position.totals)

    def test_filter_guesses_by_highest_char_occurrence(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        current_words = make_word_list_with_count(words.words)
        current_words = filter_guesses_by_highest_char_occurrence(current_words, must_chars,
                                                                  words.count_and_position)
        self.assertEqual([['WREAK', 12], ['WREST', 12], ['WRATH', 11]], current_words)

    def test_filter_guesses_by_position_in_word(self):
        data_filename = "test_answers.txt"
        words = Words(data_filename)
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        current_words = [['WREAK', 10], ['WRECK', 10], ['WREST', 10]]
        must_chars = ''
        current_words = filter_guesses_by_position_in_word(current_words, must_chars, words.count_and_position)
        self.assertEqual([['WRECK', 23], ['WREAK', 22], ['WREST', 21]], current_words)

    def test_find_matches(self):
        result = find_matches("BOOBY", "BOBBY")
        self.assertEqual("EENEE", result, )
        result = find_matches("ABABB", "BOBBY")
        self.assertEqual("NYNEY", result)
        result = find_matches("AOABB", "BOBBY")
        self.assertEqual("NENEY", result)
        result = find_matches("AAABB", "BOBBY")
        self.assertEqual("NNNEY", result)

    def test_repeated_chars(self):
        self.assertEqual("", check_repeats("ABCDE"))
        self.assertEqual("A", check_repeats("AAAAA"))
        self.assertEqual("M", check_repeats("MOMMY"))
        self.assertEqual("AL", check_repeats("ALLAY"))

    def test_create_guess(self):
        words = words_for_testing()
        words.words = ['WOUND', 'WOVEN', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST']
        words.count_chars()
        guesses = ["WOCNK"]
        matches = ["ENYNE"]
        must_chars, not_chars, not_here_chars, position_chars, repeated_chars = make_filter_values(guesses, matches)
        guesses = words.create_guess(must_chars, not_here_chars, words.count_and_position)
        Trace.write(list_to_str(guesses))
        self.assertEqual(['WREST', 'WREAK'], guesses)

    def test_server(self):
        answers_filename = "test_answers.txt"
        data_filename = "test_words.txt"
        server = Server(data_filename, answers_filename)
        server.set_answer(1)
        Trace.write("Answer is " + server.answer)
        self.assertEqual("WOUND", server.answer)
        result = server.check_guess("WORSE")
        self.assertEqual('WORSE EENNN', result)

        result = server.check_guess("WOUND")
        self.assertEqual('WOUND EEEEE', result)

    # @unittest.skip("For speed")
    def test_games(self):
        game, server = setup_game()
        Trace()
        Log()
        Trace.write("Doing test games ")
        word_map = {'FOCAL': 4, 'LOCAL': 4, 'STATE': 4, 'STEAK': 3, 'TEASE': 3, 'VOCAL': 4, 'YEAST': 3, 'LEAST': 3,
                    'STAVE': 4, 'TRUSS': 3, 'TRUST': 3, 'CRUST': 3, 'SWEAT': 3, 'POUND': 4, 'PRIZE': 4, 'SHAVE': 4,
                    'SHARE': 3, 'SNARE': 3, 'SPARE': 3, 'TAUNT': 5, 'JAUNT': 5, 'HAUNT': 4, 'GAUNT': 4, 'VAUNT': 5,
                    'WATCH': 5, 'WIGHT': 5, 'WINCH': 5, 'WOUND': 4, 'GRAZE': 4, 'SNAIL': 4, 'SKUNK': 4, 'STEER': 3,
                    'ESTER': 3, 'RESET': 3, 'TONIC': 4, 'GEESE': 3, 'ERROR': 4, 'FEMME': 4, 'FREER': 5}
        print("---Test Games ----")
        new_map = {}
        previous_total_turns = 0
        total_turns = 0
        for index, word in enumerate(word_map):
            previous_turns = word_map[word]
            previous_total_turns += previous_turns
            t = Timer()
            t.start()
            turns = test_game(word, game, server)
            print("Word ", word, " turns ", turns, " previous turns ", previous_turns)
            new_map[word] = turns
            if turns != previous_turns:
                print("** Better or worse ? ")
            total_turns += turns
            self.assertLess(turns, 7, " For word " + word)
        print(" Total turns ", total_turns, " previous total turns ", previous_total_turns)
        # print(new_map)
        self.assertEqual(previous_total_turns, total_turns)
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
