from GameRound import *
from server import *
from Log import *
from timer import Timer


def run_a_game(game, server):
    guesses = []
    matches = []
    turns = 0
    guess = game.get_guess(guesses, matches)

    for i in range(7):
        turns += 1
        guess, match = server_guess_match(server, guess)
        Log.write("Guess " + guess + " match " + match)
        Trace.write("Guess " + guess + " match " + match)
        guesses.append(guess)
        matches.append(match)
        guess = game.get_guess(guesses, matches)
        if match == 'EEEEE':
            break
    Trace.write("---Answer is " + server.answer + " in turns " + str(turns))
    if turns > 6:
        Log.write("*** word " + server.answer + " not found ")
        Trace.write("*** word " + server.answer + " not found ")
    return turns


def server_guess_match(server, guess):
    inp = server.check_guess(guess)
    (guess, match) = inp.split(' ')
    return guess, match


def input_guess_match():
    good = False
    guess = ""
    match = ""

    while not good:
        inp = input("Guess result")
        print(inp)
        (guess, match) = inp.split(' ')
        if len(guess) == 5 and len(match) == 5:
            good = True

    return guess, match


def main():
    # args = sys.argv[1:]
    # if len(args) < 2:
    # sys.exit( "NeedTwoArguments" + " <word_filename>  <answers_filename" )
    # data_filename = args[0]
    # answers_filename = args[1]
    log = Log("log_GamePlayer.txt")
    trace = Trace("trace_GamePlayer.txt")
    data_filename = "words002.txt"
    answers_filename = "answers.txt"
    game = GameRound(data_filename, answers_filename)
    server = Server(data_filename, answers_filename)
    total_turns = 0
    turn_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    t = Timer()
    t.start()
    for i in range(len(game.answers.words)):
        server.set_answer(i + 1)
        Log.write("-----Answer= " + server.answer)
        Trace.write("-----Answer -----" + server.answer)
        turns = run_a_game(game, server)
        print("Answer " + server.answer + " Turns " + str(turns))
        if turns < len(turn_counts):
            turn_counts[turns - 1] += 1
        else:
            Trace.write("***Turns too many")
        total_turns += turns
    elapsed = t.stop()
    print("Elapsed time is ", elapsed)
    print("Turn counts ", list_to_str(turn_counts))
    average = total_turns / len(game.answers.words)
    Log.write("Average is " + str(average))
    Trace.write("Turn counts " + str(turn_counts))
    log.close()
    trace.close()


if __name__ == "__main__":
    main()
