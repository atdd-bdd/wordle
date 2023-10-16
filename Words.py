import sys
import os
from filter import *
from Log import *
from CountAndPosition import *


def list_to_str(a_list):
    if len(a_list) <= 50:
        return ' '.join([str(elem) for elem in a_list])
    else:
        out = "[" + str(len(a_list)) + "] "
        for index in range(50):
            out += ' ' + a_list[index]
        return out


def list_list_to_str(a_list):
    maxy = len(a_list)
    if maxy > 50:
        maxy = 50
    out = "[" + str(len(a_list)) + "] "
    for index in range(maxy):
        out += ' ' + str(a_list[index][0]) + '=' + str(a_list[index][1])
    return out




def make_word_list_with_count(words):
    out_words = []
    for word in words:
        out_words.append([word, 0])
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
        for word in self.words:
            self.word_map[word] = 1

    def print(self):
        for word in self.words:
            Trace.write(word)

    def count(self):
        return len(self.words)

    def count_chars(self):
        self.count_and_position = CountAndPosition(self.words)

    def create_filtered_words(self, position_chars, must_chars, not_chars, not_here_chars):
        ret = Words()
        ret.words = filter_list(self.words, position_chars, must_chars, not_chars, not_here_chars)
        return ret

    def create_guess(self, must_chars, not_here_chars, count_and_position):
        current_words_with_count = make_word_list_with_count(self.words)
        current_words_with_count = filter_guesses_by_highest_char_occurrence(current_words_with_count, must_chars,
                                                                             count_and_position)
        current_words_with_count = filter_guesses_by_position_in_word(current_words_with_count,
                                                                      must_chars, count_and_position)
        current_words_with_count = filter_guesses_by_not_here_in_word(current_words_with_count,
                                                                      must_chars, not_here_chars, count_and_position)
        current_words = make_word_list_without_count(current_words_with_count)
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


def filter_guesses_by_position_in_word(current_words_with_count, must_chars, count_and_position):
    if len(current_words_with_count) <= 1:
        return current_words_with_count
    out_words = []
    count_and_position.zero_in_totals(must_chars)
    max_position_score = 0
    for item in current_words_with_count:
        word = item[0]
        position_score = count_and_position.score_on_position_counts(word)
        score = item[1] + position_score
        out_words.append([word, score])
        if score > max_position_score:
            max_position_score = score
    Trace.write("Max position score is " + str(max_position_score))
    if max_position_score == 0:
        Trace.write("@@@ No scoring by char position")
        return current_words_with_count
    out_words = filter_by_percentage_maximum(out_words, max_position_score, 99)
    return out_words


def filter_guesses_by_not_here_in_word(current_words_with_count, must_chars, not_here_chars, count_and_position):
    if len(current_words_with_count) <= 1:
        return current_words_with_count
    out_words = []
    count_and_position.zero_in_totals(must_chars)
    max_position_score = -1000
    for item in current_words_with_count:
        word = item[0]
        position_score = score_on_not_here_counts(word, not_here_chars, count_and_position.positions)
        score = item[1] + position_score
        out_words.append([word, score])
        if score > max_position_score:
            max_position_score = score
    Trace.write("Max not here score is " + str(max_position_score))
    if max_position_score == -1000:
        Trace.write("@@@ No scoring by not here position")
        return current_words_with_count
    out_words = filter_by_percentage_maximum(out_words, max_position_score, 99)
    return out_words


def filter_by_percentage_maximum(current_words, max_total_score, percentage):
    cutoff = (max_total_score * percentage) / 100
    Trace.write("Cutoff is " + str(cutoff))
    out_words = []
    for item in current_words:
        if item[1] >= cutoff:
            out_words.append(item)

    Trace.write("Words by highest maximum " + str(percentage) + " " + list_list_to_str(out_words))
    return out_words


def filter_guesses_by_highest_char_occurrence(current_words, must_chars, count_and_position):
    if len(current_words) <= 1:
        return current_words
    Trace.write("Must chars " + must_chars)
    count_and_position.zero_in_totals(must_chars)

    max_total_score = 0
    out_words = []
    for item in current_words:
        word = item[0]
        total_score = count_and_position.score_on_totals(word)
        out_words.append([word, total_score])
        # print("Word ", word, " Total ", total_score)
        if total_score > max_total_score:
            max_total_score = total_score

    Trace.write("Max score is " + str(max_total_score))
    if max_total_score == 0:
        Trace.write("@@@ No words found in by high chars")
        return []
    out_words = filter_by_percentage_maximum(out_words, max_total_score, 99)
    return out_words


def exit_with_message(message):
    sys.exit(message)





def compute_rating(word, look_for):
    values = [10, 8, 6, 4, 2]
    value = 0
    for c in word:
        for i in range(len(look_for)):
            if c == look_for[i]:
                value += values[i]
    return value
