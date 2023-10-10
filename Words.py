import sys
import os
from filter import *
from Log import *


def list_to_str(a_list):
    return ' '.join([str(elem) for elem in a_list])


def filter_words_by_rating(filtered_words, look_for):
    rated_words = []
    max_rating = 0
    for word in filtered_words:
        rating = compute_rating(word, look_for)
        if rating > max_rating:
            max_rating = rating

    for word in filtered_words:
        rating = compute_rating(word, look_for)
        if rating == max_rating:
            rated_words.append(word)
    return rated_words


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
        for word in self.words:
            for i in range(5):
                index = ord(word[i]) - ord('A')
                self.char_counts_in_position[index][i] += 1
                self.char_counts_total[word[i]] += 1

    def print_count_chars(self):
        for i in range(26):
            Trace.write(chr(i + ord('A')) + " " + str(self.char_counts_total[chr(i + ord('A'))]))

            Trace.write(str(self.char_counts_in_position[i][0]) + " " + str(self.char_counts_in_position[i][1]) + " " +
                        str(self.char_counts_in_position[i][2]) + " " + str(self.char_counts_in_position[i][3]) + " " +
                        str(self.char_counts_in_position[i][4]))

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
            if self.char_counts_total[key] > 0:
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

    def create_guess_from_self(self, not_here_chars, position_chars, must_chars):
        Trace.write(" Creating guess from filtered answer list ")
        Trace.write("Words " + list_to_str(self.words))
        Trace.write("Not here " + list_to_str(not_here_chars))
        Trace.write("Position chars " + list_to_str(position_chars))
        if count_position_chars(position_chars) != 4:
            return self.determine_guess_from_filtered_list(must_chars)
        else:
            chars_to_be_in_word = determine_word_with_all_characters(self.words, position_chars)
            return chars_to_be_in_word, False

    def determine_guess_from_filtered_list(self, must_chars):
        Trace.write("Determining guess from filtered list ")
        temp = Words()
        temp.words = self.words
        temp.count_chars()
        sorted_values = temp.sorted_count_chars()
        ret = filter_guesses_by_highest_char_occurance(temp.words, must_chars, sorted_values)
        return ret[0], True

    last_must_char_guess_index = 0

    def create_guess(self, sorted_values, must_chars, sorted_char_counts_in_position):
        current_words = self.words
        current_words = filter_guesses_by_highest_char_occurance(current_words, must_chars, sorted_values)
        current_words = filter_guesses_by_position_in_word(current_words, sorted_char_counts_in_position,
                                                           sorted_values)
        return current_words[0]

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


def filter_guesses_by_position_in_word(current_words, sorted_char_counts_in_position, sorted_values):
    current_word = current_words[0]
    max_count = 0
    if len(current_words) > 1:
        for word in current_words:
            count = 0
            number_matches = 0
            for i in range(len(word)):
                c = word[i]
                position = find_in_counts(sorted_char_counts_in_position, c)
                if position == i:
                    value = find_sort_value_weight(sorted_values, c)
                    count += value
                    number_matches += 1
            if count > max_count:
                max_count = count
                current_word = word
    Trace.write("Current word by position " + current_word)
    current_words = [current_word]
    return current_words


def filter_guesses_by_highest_char_occurance(current_words, must_chars, sorted_values):
    look_for = []
    words_with_matches = [[], [], [], [], [], []]
    Trace.write("Must chars " + must_chars)

    look_for = shrink_number_to_look_for(look_for, must_chars, sorted_values)
    filtered_words = []

    for word in current_words:
        match_count = 0
        for c in look_for:
            if c in word:
                match_count += 1
        words_with_matches[match_count].append(word)

    for i in range(6):
        index = 5 - i
        if len(words_with_matches[index]) > 0:
            filtered_words = words_with_matches[index]
            break
    Trace.write("Filtered words of this list " + list_to_str(filtered_words))
    rated_words = filter_words_by_rating(filtered_words, look_for)
    Trace.write("Rated words " + list_to_str(rated_words))

    return rated_words


def shrink_number_to_look_for(look_for, must_chars, sorted_values):
    number_to_look_for = 0
    for c in sorted_values:
        if c in must_chars:
            # Trace.write(" Skipping ", c)
            continue
        look_for += c
        number_to_look_for += 1
        if number_to_look_for > 4:
            break
    Trace.write("Looking for " + list_to_str(look_for))
    return look_for


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
    return e[1]  # the count


def compute_rating(word, look_for):
    values = [10, 8, 6, 4, 2]
    value = 0
    for c in word:
        for i in range(len(look_for)):
            if c == look_for[i]:
                value += values[i]
    return value
