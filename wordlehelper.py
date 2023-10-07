from GameRound import *


def main():
	args = sys.argv[1:]
	if len(args) < 2:
		sys.exit( "NeedTwoArguments" + " <word_filename>  <answers_filename" )

	data_filename = args[0]
	answers_filename = args[1]
	game = GameRound(data_filename, answers_filename)
	guesses = []
	matches = []
	guess = game.get_guess(guesses, matches)
	print("initial", guess)
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
