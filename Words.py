import sys
import os

from filter import *
from CountAndPosition import *
from timer import Timer
from utilities import list_list_to_str, sort_function, list_to_str


def make_word_list_with_count(words):
    out_words = []
    for word in words:
        out_words.append((word, 0))
    return out_words


def make_word_list_without_count(words_with_count):
    out_words = []
    for item in words_with_count:
        out_words.append(item[0])
    return out_words


class Words:

    def __init__(self, data_filename=""):
        self.inited = False
        self.data_filename = data_filename
        self.words = []
        self.word_map = {}
        self.count_and_position = CountAndPosition(self.words)

    def first_word(self):
        if len(self.words) >= 1:
            return self.words[0]
        return "ZZZZZ"

    def length_words(self):
        return len(self.words)

    def read_words(self):
        self.read_words_from_file()

        for word in self.words:
            self.word_map[word] = 1

    def read_words_from_file(self):
        if not os.path.isfile(self.data_filename):
            exit_with_message("FileNotExist")
        with open(self.data_filename, encoding='utf-8') as f:
            in_words = f.readlines()
            for i in range(len(in_words)):
                word = in_words[i].strip()
                self.words.append(word.upper())
            last_word = len(self.words)
            for i in reversed(range(last_word)):
                if len(self.words[i]) < 1:
                    self.words.pop(i)
                else:
                    break
        if len(self.words) < 1:
            exit_with_message("EmptyFile")

    def print(self):
        for word in self.words:
            Trace.write(word)

    def count(self):
        return len(self.words)

    def count_chars(self):
        self.count_and_position = CountAndPosition(self.words)

    def create_filtered_words(self, position_chars, must_chars, not_chars, not_here_chars, repeated_chars):
        ret = Words()
        ret.words = filter_list(self.words, position_chars, must_chars, not_chars, not_here_chars,
                                repeated_chars)
        return ret

    def create_guess(self, must_chars, not_here_chars, count_and_position):
        tall = Timer()
        tall.start()
        t1 = Timer()
        t1.start()
        current_words = self.words
        if Configuration.hard_mode:
            current_words = filter_list(current_words, ["", "", "", "", ""], must_chars, "",
                                    ["", "", "", "", ""], "")
            Trace.write("Filtered current words " + list_to_str(current_words))
        current_words_with_count = make_word_list_with_count(current_words)
        # Trace.write(" Making word list time " + t1.stop())
        t2 = Timer()
        t2.start()

        Trace.write("Filter by highest char occurrence")
        current_words_with_count = filter_guesses_by_highest_char_occurrence(current_words_with_count, must_chars,
                                                                             count_and_position)
        # Trace.write("Filter by highest occurrence  " + t2.stop())
        Trace.write("Filter by highest pair occurrence")
        current_words_with_count = filter_guesses_by_highest_pair_occurrence(current_words_with_count,
                                                                             count_and_position)

        Trace.write("Filter by position in word ")
        current_words_with_count = filter_guesses_by_position_in_word(current_words_with_count,
                                                                      must_chars, count_and_position)
        # Trace.write(" Filter by position in word  " + t3.stop())
        Trace.write("Filtered by not here in word")
        current_words_with_count = filter_guesses_by_not_here_in_word(current_words_with_count,
                                                                      must_chars, not_here_chars, count_and_position)

        current_words_with_count.sort(reverse=True, key=sort_function)
        current_words = make_word_list_without_count(current_words_with_count)
        # Trace.write(" Total guess time  " + tall.stop())

        return current_words

    def find_answer(self, word_index):
        index = word_index
        if index < 1 or index > len(self.words):
            exit_with_message("WordIndexOutOfRange")
        answer = self.words[index - 1]
        if len(answer) < 1:
            exit_with_message("AnswerNotValid ")
        return answer

    def check_guess(self, guess):
        # Check guess in the list
        value = self.word_map.get(guess)
        if value is None:
            return False
        return True


def determine_word_with_all_characters(words, position_chars):
    to_check = 0
    for i in range(len(position_chars)):
        if len(position_chars[i]) == 0:
            Trace.write("Unknown is " + str(i))
            to_check = i
            break
    might_have_chars = ""
    for word in words:
        might_have_chars += word[to_check]
    Trace.write("Might have chars " + list_to_str(might_have_chars))
    return might_have_chars


def count_position_chars(position_chars):
    size = 0
    for s in position_chars:
        if len(s) > 0:
            size += 1
    Trace.write("Size of position chars " + str(size))
    return size


def filter_by_percentage_maximum(current_words, max_total_score, percentage):
    cutoff = (max_total_score * percentage) / 100
    # Trace.write("Cutoff is " + str(cutoff))
    out_words = []
    if len(current_words) < Configuration.minimum_to_filter:
        current_words.sort(reverse=True, key=sort_function)
        return current_words
    for item in current_words:
        if item[1] >= cutoff:
            out_words.append(item)
    out_words.sort(reverse=True, key=sort_function)
    Trace.write(list_list_to_str(out_words))
    return out_words


def filter_guesses_by_highest_char_occurrence(current_words, must_chars, count_and_position):
    if len(current_words) <= 1:
        return current_words
    t1 = Timer()
    t1.start()
    # Trace.write("Must chars " + must_chars)
    if not Configuration.hard_mode:
        count_and_position.zero_in_totals(must_chars)

    max_total_score = 0
    out_words = []
    # Trace.write("First part " + t1.stop())
    t2 = Timer()
    t2.start()
    for item in current_words:
        word = item[0]
        score = count_and_position.score_on_totals(word)
        if Configuration.high_char_add_to_previous:
            total_score = item[1] + score
        else:
            total_score = score
        out_words.append((word, total_score))
        if total_score > max_total_score:
            max_total_score = total_score
    # Trace.write("Second part " + t2.stop())
    # Trace.write("Max score is " + str(max_total_score))
    if max_total_score == 0:
        Trace.write("@@@ No words found in by high chars")
        return []
    out_words = filter_by_percentage_maximum(out_words, max_total_score, Configuration.cutoff_high_char)
    return out_words


def filter_guesses_by_highest_pair_occurrence(current_words, count_and_position):
    if len(current_words) <= 1:
        return current_words
    max_total_score = 0
    out_words = []
    for item in current_words:
        word = item[0]
        score = count_and_position.score_on_pair_occurance(word)
        if Configuration.two_letter_add_to_previous:
            total_score = item[1] + score
        else:
            total_score = score
        out_words.append((word, total_score))
        if total_score > max_total_score:
            max_total_score = total_score
    out_words = filter_by_percentage_maximum(out_words, max_total_score, Configuration.two_letter_add_to_previous)
    return out_words


def filter_guesses_by_position_in_word(current_words_with_count, must_chars, count_and_position):
    if len(current_words_with_count) <= 1:
        return current_words_with_count
    out_words = []
    count_and_position.zero_in_totals(must_chars)
    max_position_score = 0
    for item in current_words_with_count:
        word = item[0]
        score = count_and_position.score_on_position_counts(word)
        if Configuration.position_add_to_previous:
            total_score = item[1] + score
        else:
            total_score = score
        out_words.append((word, total_score))
        if total_score > max_position_score:
            max_position_score = total_score
    # Trace.write("Max position total_score is " + str(max_position_score))
    if max_position_score == 0:
        Trace.write("@@@ No scoring by char position")
        return current_words_with_count
    out_words = filter_by_percentage_maximum(out_words, max_position_score, Configuration.cutoff_position)
    return out_words


def filter_guesses_by_not_here_in_word(current_words_with_count, must_chars, not_here_chars, count_and_position):
    if len(current_words_with_count) <= 1:
        return current_words_with_count
    out_words = []
    count_and_position.zero_in_totals(must_chars)
    max_position_score = -1000
    for item in current_words_with_count:
        word = item[0]
        score = score_on_not_here_counts(word, not_here_chars, count_and_position.positions)
        if Configuration.not_there_add_to_previous:
            total_score = item[1] + score
        else:
            total_score = score
        out_words.append((word, total_score))
        if total_score > max_position_score:
            max_position_score = total_score
    # Trace.write("Max not here score is " + str(max_position_score) + " not here chars " +
    #             list_to_str_with_quotes(not_here_chars))
    if max_position_score == -1000:
        Trace.write("@@@ No scoring by not here position")
        return current_words_with_count
    out_words = filter_by_percentage_maximum(out_words, max_position_score, Configuration.cutoff_not_there)
    return out_words


def exit_with_message(message):
    sys.exit(message)
