
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

	def find_answer(self, word_index):
		index = word_index
		if index < 1 or index > len(self.words):
			exit_with_message("WordIndexOutOfRange")
		answer = self.words[index - 1]
		if len(answer) < 1:
			exit_with_message("AnswerNotValid ")
		return answer


	def check_guess(self, guess):
		# Check the guess
		if len(guess) < 1:
			exit_with_message("SizeOfGuessInvalid")
		found = False
		for word in self.words:
			if guess == word:
				found = True
				break
		if not found:
			exit_with_message( guess + " " + "NotAWord")

	def determine_match(self, word_index, guess):
		answer=self.find_answer(word_index)
		self.check_guess(guess)
		match = find_matches(guess, answer)
		exit_with_message(guess + " " + match)

	def print(self):
		for word in self.words:
			print (word)

	def count(self):
		return len(self.words)

	def count_chars(self):
		for word in self.words:
			chars = []
			for i in range(5):
				index = ord(word[i])- ord('A')
				self.char_counts_in_position[index][i] += 1
				self.char_counts_total[word[i]] += 1
	def print_count_chars(self):
		for i in range(26):
			print (chr(i + ord('A')), " " , self.char_counts_total[chr(i + ord('A'))])

			print(self.char_counts_in_position[i][0], " ", self.char_counts_in_position[i][1], " ", self.char_counts_in_position[i][2], " ", self.char_counts_in_position[i][3], " ", self.char_counts_in_position[i][4])


	def sorted_count_chars(self):
		values = []
		for key in self.char_counts_total:
			values.append([key,self.char_counts_total[key]] )
		values.sort(key=sort_function,reverse=True)
		#print(values)
		sorted_values = []

		for value in values:
			sorted_values.append(value[0])
		return sorted_values

	def create_filtered_words(self, position_chars, must_chars, not_chars, not_here_chars):
		ret = Words()

		ret.words = filter_list(self.words, position_chars, must_chars, not_chars, not_here_chars)

		return ret

	def create_guess(self, sorted_values, must_chars, not_here_chars):
		current_guess = ""
		##print("Create guess")
		#print(sorted_values)
		current_words = self.words
		for iteration in range(1):
			for c in sorted_values:
				filtered_words = []
				#print("Looking at ", c)
				if (must_chars.__contains__(c)):
					#print("Word contains a must char ", c)
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
				#print(len(filtered_words))
				#print (filtered_words)
				if len(filtered_words) > 1:
					current_words = filtered_words
				else:
					#print (current_words)
					break
		return current_words



def sort_function(e):
	#print(e[0], e[1])
	return e[1]    # the count