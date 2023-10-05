

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
		a = ' ';
		if (i < answer_size):
			a = answer[i]
		if (g==a):
			matches[i]=value_EXACT_MATCH
			continue
		for j in range(answer_size):
			a = answer[j]
			if (g==a):
				matches[i]= value_IN_WORD_MATCH
				break
	match = "".join(matches)
	return match


def get_random_index(game_set, word_index, words_size, words_to_score):
	if word_index > words_to_score or word_index < 1:
		exit_with_message( "WordIndexOutOfRange")
	if words_to_score < 1:
		return 1
	if game_set < 0:
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




