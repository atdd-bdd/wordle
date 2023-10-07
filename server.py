
import sys
import os
from Words import *

class Server:
	def __init__(self, all_words_filename, answers_filename):
		self.all_words = Words(all_words_filename)
		self.all_words.read_words()
		print(" Length of ", all_words_filename, " ", self.all_words.count())
		self.answers = Words(answers_filename)
		self.answers.read_words()
		print(" Length of ", answers_filename, " ", self.answers.count())
		self.answer = "ZZZZZ"

	def set_answer(self, index):
		self.answer = self.answers.find_answer(index)

	def check_guess(self, guess):
		result = self.all_words.check_guess(guess)
		if not result:
			return guess + " " + "NotAWord"
		else:
			result = find_matches(guess, self.answer)
			return guess + " " + result

def find_matches(guess, answer):
	value_NO_MATCH = 'N'
	value_IN_WORD_MATCH = 'Y'
	value_EXACT_MATCH = 'E'
	guess_size = len(guess)
	answer_size = len(answer) 
	matches= [value_NO_MATCH for i in range(guess_size)]
	last_answer_index = answer_size - 1
	last_guess_index = guess_size - 1 

	for i in range(guess_size):
		g = guess[i]
		a = ' '
		if i < answer_size:
			a = answer[i]
		if g==a:
			matches[i]=value_EXACT_MATCH
			continue
		for j in range(answer_size):
			a = answer[j]
			if g==a:
				matches[i]= value_IN_WORD_MATCH 
				break 
	match = "".join(matches)
	return match




def get_random_index(game_set, word_index, words_size, words_to_score):
	if (word_index > words_to_score or word_index < 1): 
		exit_with_message( "WordIndexOutOfRange")
	if (words_to_score < 1): 
		return 1
	if (game_set < 0): 
		game_set = -game_set
	r = simple_rand(game_set , words_size, word_index) 
	new_word_index = r + 1
	return new_word_index 


def simple_rand(seed, max_value, index):
	mult = 389 
	add = 397 
	random = seed
	for i in range(0,index):
		random = ((random * mult) + add ) % max_value
	return random 


def main():
	###   Needs work to become standalone -
	args = sys.argv[1:]
	if (len(args) < 3):
		exit_with_message( "NeedThreeArguments" + " <word_filename> <word_index>  <guess>" )
	game_set = 0 
	words_to_score = 0
	if (len(args) == 4):
		exit_with_message( "NeedFiveArguments" + " <word_filename> <word_index>  <guess> <game_set> <words_to_score>" )
	if (len(args) >= 5): 
		game_set = int(args[3], base=10)
		words_to_score = int(args[4], base=10)
	data_filename = args[0]
	word_index = int(args[1], base=10)
	guess = args[2]
	words = read_words(data_filename)
	if (game_set > 0): 
		word_index = get_random_index(game_set, word_index, len(words), words_to_score)
	determine_match(words, word_index, guess)

#	os.system("dir > temp.txt")


if __name__ == "__main__":
	main()
