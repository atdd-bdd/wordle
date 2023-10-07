from GameRound import *
from server import *
from Log import *

def main():
    # args = sys.argv[1:]
    # if len(args) < 2:
    # sys.exit( "NeedTwoArguments" + " <word_filename>  <answers_filename" )
    # data_filename = args[0]
    # answers_filename = args[1]
    x =Log()
    data_filename = "words002.txt"
    answers_filename = "answers.txt"
    game = GameRound(data_filename, answers_filename)
    server = Server(data_filename, answers_filename)
    total_turns = 0
    turn_counts = [0,0,0,0,0,0,0,]
    max = 0
    for i in range(len(game.answers.words)):
        turns =  run_a_game(game, server, i + 1)
        if turns < len(turn_counts):
            turn_counts[turns-1] += 1
        else:
            print(" Turns too many ")
        total_turns += turns
        if (turns > max):
            max = turns
        Log.write("Average = " +  str(total_turns / (i + 1)) +  " Max is " + str( max))
    average = total_turns / len(game.answers.words)
    Log.write("Average is " + str(average))
    print(" turn counts ", turn_counts)



def run_a_game(game, server, index):
    server.set_answer(index)
    Log.write("Answer is " +server.answer)
    guesses = []
    matches = []
    turns = 0
    guess = game.get_guess(guesses, matches)

    for i in range(7):
        turns += 1
        guess, match = server_guess_match(server, guess)
        Log.write("Guess " + guess +  " match " +  match)
        guesses.append(guess)
        matches.append(match)
        guess = game.get_guess(guesses, matches)

        if match == "EEEEE":
            break
    print("Answer is " + server.answer, " turns ", turns)

    return turns

def server_guess_match(server, guess):
    good = False
    match = ""
    inp = server.check_guess(guess)
    (guess, match) = inp.split(' ')
    return guess, match

def input_guess_match():
    good = False
    guess = ""
    match = ""

    while (not good):
        inp = input("Guess result")
        print(inp)
        (guess, match) = inp.split(' ')
        if len(guess) == 5 and len(match) == 5:
            good = True

    return guess, match
