from Words import *
class GameRound:
	def __init__(self, all_words_filename, answers_filename):
		self.all_words = Words(all_words_filename)
		self.all_words.read_words()
		print(" Length of " + all_words_filename)
		print(self.all_words.count())
		self.all_words.count_chars()
		self.all_words.sorted_count_chars()
		self.answers = Words(answers_filename)
		self.answers.read_words()
		# print(" Length of " + answers_filename)
		# print(answers.count())
		self.answers.count_chars()

		# answers.print_count_chars()

		self.answers.sorted_count_chars()
	def get_guess(self, guesses, matches):
		must_chars, not_chars, not_here_chars, position_chars = make_filter_values(guesses, matches)
		# print("Results")
		# print("Exact", position_chars)
		# print("Must ", must_chars)
		# print("Not ", not_chars)
		# for not_here_char in not_here_chars:
		#	print(not_here_char)

		filtered = self.answers.create_filtered_words(position_chars, must_chars, not_chars, not_here_chars)
		filtered.count_chars()
		sorted_values = filtered.sorted_count_chars()
		# print(sorted_values)
		guess = self.all_words.create_guess(sorted_values, must_chars, not_here_chars)
		return guess

def exit_with_message(message):
	sys.exit(message)
def main():
	args = sys.argv[1:]
	if len(args) < 2:
		exit_with_message( "NeedTwoArguments" + " <word_filename>  <answers_filename" )

	data_filename = args[0]
	answers_filename = args[1]
	game = GameRound(data_filename, answers_filename)
	guesses = []
	matches = []
	for i in range(6):
		guess, match = input_guess_match()
		guesses.append(guess)
		matches.append(match)
		guess = game.get_guess(guesses, matches)
		print(guess)


def input_guess_match():
	good = False
	guess =""
	match = ""
	while (not good):
		inp = input("Guess result")
		print(inp)
		(guess, match) = inp.split(' ')
		if len(guess) == 5 and len(match) == 5:
			good = True

	return guess, match


##guess  = input("Guess result")
	##print (guess)


#	os.system("dir > temp.txt")


if __name__ == "__main__":
	main()
