import sys
import os
from filter import *


class Words:

    def __init__(self, data_filename=""):
        self.inited = False
        self.data_filename = data_filename
        self.words = []
        self.char_counts_in_position = []
        for i in range(26):
            self.char_counts_in_position.append([0, 0, 0, 0, 0])
        self.char_counts_total = {}
        for i in range(26):
            self.char_counts_total[chr(i + ord('A'))] = 0
        self.word_map = {}

    def first_word(self):
        if len(self.words) >= 1:
            return self.words[0]
        return "ZZZZZ"

    def length_words(self):
        return len(self.words)

    def read_words(self):
        if not os.path.isfile(self.data_filename):
            exit_with_message("FileNotExist")
        words = []
        with open(self.data_filename, encoding='utf-8') as f:
            inwords = f.readlines()
            for i in range(len(inwords)):
                word = inwords[i].strip()
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
            print(word)

    def count(self):
        return len(self.words)

    def count_chars(self):
        for word in self.words:
            chars = []
            for i in range(5):
                index = ord(word[i]) - ord('A')
                self.char_counts_in_position[index][i] += 1
                self.char_counts_total[word[i]] += 1

    def print_count_chars(self):
        for i in range(26):
            print(chr(i + ord('A')), " ", self.char_counts_total[chr(i + ord('A'))])

            print(self.char_counts_in_position[i][0], " ", self.char_counts_in_position[i][1], " ",
                  self.char_counts_in_position[i][2], " ", self.char_counts_in_position[i][3], " ",
                  self.char_counts_in_position[i][4])

    def sort_char_counts_in_position(self):
        sorted_char_counts_in_position = []
        for k in range(len(self.char_counts_in_position)):
            char_counts_in_a_position = self.char_counts_in_position[k]
            max_count_index = 0
            max_count = 0
            for i in range(5):
                if char_counts_in_a_position[i] > max_count:
                    max_count_index = i
                    max_count = char_counts_in_a_position[i]
            sorted_char_counts_in_position.append([chr(k + ord('A')), max_count_index])
        return sorted_char_counts_in_position

    def sorted_count_chars(self):
        values = []
        for key in self.char_counts_total:
            values.append([key, self.char_counts_total[key]])
        values.sort(key=sort_function, reverse=True)
        sorted_values = []
        for value in values:
            sorted_values.append(value[0])
        self.sort_char_counts_in_position()
        return sorted_values

    def create_filtered_words(self, position_chars, must_chars, not_chars, not_here_chars):
        ret = Words()
        ret.words = filter_list(self.words, position_chars, must_chars, not_chars, not_here_chars)
        return ret

    def create_guess(self, sorted_values, must_chars):
        current_words = self.words
        current_words = self.filter_guesses_by_highest_char_occurance(current_words, must_chars, sorted_values)
        current_words = self.filter_guesses_by_position_in_word(current_words, self.sort_char_counts_in_position(),
                                                                sorted_values)

        return current_words

    def filter_guesses_by_highest_char_occurance(self, current_words, must_chars, sorted_values):
        for c in sorted_values:
            filtered_words = []
            if must_chars.__contains__(c):
                continue
            word_to_add = ""
            for word in current_words:
                keeper = False
                for d in word:
                    if c == d:
                        keeper = True
                        word_to_add = word
                        break
                if keeper:
                    filtered_words.append(word_to_add)

            if len(filtered_words) > 1:
                current_words = filtered_words
            else:
                break
        return current_words

    def filter_guesses_by_position_in_word(self, current_words, sorted_char_counts_in_position, sorted_values):
        current_word = current_words[0]
        max_count = 0
        if len(current_words) > 1:
            for word in current_words:
                count = 0
                for i in range(len(word)):
                    c = word[i]
                    position = find_in_counts(sorted_char_counts_in_position, c)
                    if position == i:
                        value = find_sort_value_weight(sorted_values, c)
                        count += value
                if count > max_count:
                    max_count = count
                    current_word = word
        current_words = [current_word]
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

    def determine_match(self, word_index, guess):
        answer = self.find_answer(word_index)
        self.check_guess(guess)
        match = find_matches(guess, answer)
        exit_with_message(guess + " " + match)


def find_in_counts(sorted_char_counts_in_position, c):
    for i in range(len(sorted_char_counts_in_position)):
        if sorted_char_counts_in_position[i][0] == c:
            return sorted_char_counts_in_position[i][1]
    return 0


def find_sort_value_weight(sorted_values, c):
    for i in range(len(sorted_values)):
        if c == sorted_values[i]:
            return len(sorted_values) - i + 1
    return 0


def exit_with_message(message):
    sys.exit(message)


def sort_function(e):
    # print(e[0], e[1])
    return e[1]  # the count
