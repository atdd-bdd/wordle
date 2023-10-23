from GameRound import *
from Log import *
from server import *
from timer import Timer


def play_full_game_with_first_guess(first_guess=""):
    data_filename = Configuration.data_filename
    answers_filename = Configuration.answer_filename
    Trace.write(Configuration.get_files())
    game = GameRound(data_filename, answers_filename)
    server = Server(data_filename, answers_filename)
    total_turns = 0
    turn_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    t = Timer()
    t.start()
    word_count = game.answers.words
    for i in range(len(word_count)):
        server.set_answer(i + 1)
        Log.write("---Answer= " + server.answer)
        Trace.write("---Answer=" + server.answer)
        turns = run_a_game(game, server, first_guess)
        # print("Answer " + server.answer + " Turns " + str(turns))
        if turns < len(turn_counts):
            turn_counts[turns - 1] += 1
        else:
            Trace.write("*** Turns too many")
            print("*** Turns too many ")
        total_turns += turns
    elapsed = t.stop()
    print("Elapsed time is ", elapsed)
    print("Turn counts ", list_to_str(turn_counts))
    average = total_turns / len(word_count)
    print('average ' + round_to_string(average), " first guess ", first_guess)
    Log.write("Average is " + round_to_string(average))
    Trace.write("Turn counts " + list_to_str(turn_counts))
    ResultLog.write(
        "Turn counts " + list_to_str(turn_counts) + " Average is " + round_to_string(average) + " first guess " +
        first_guess)
    ResultLog.write(elapsed)
    return average


def run_a_game(game, server, first_guess=""):
    guesses = []
    matches = []
    turns = 0

    if first_guess != "":
        guess = first_guess
    else:
        guess = game.get_guess(guesses, matches)
    for _ in range(7):
        turns += 1
        guess, match = server_guess_match(server, guess)
        Log.write("Guess " + guess + " match " + match)
        Trace.write("Turn " + str(turns) + " Guess " + guess + " result match " + match)
        if match == 'EEEEE':
            break
        guesses.append(guess)
        matches.append(match)
        guess = game.get_guess(guesses, matches)
    Trace.write("---Answer=" + server.answer + " in turns " + str(turns))
    if turns > 6:
        Log.write("*** word " + server.answer + " not found ")
        Trace.write("*** word " + server.answer + " not found ")
    return turns


def round_to_string(a):
    b = f"{a: .5f}"
    return b


def server_guess_match(server, guess):
    inp = server.check_guess(guess)
    (guess, match) = inp.split(' ')
    return guess, match


def input_guess_match():
    good = False
    guess = ""
    match = ""

    while not good:
        inp = input("Enter guess result:")
        print(inp)
        (guess, match) = inp.split(' ')
        if len(guess) == 5 and len(match) == 5:
            good = True

    return guess, match
