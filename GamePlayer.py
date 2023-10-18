from GameRound import *
from server import *
from Log import *
from timer import Timer


def round_to_string(a):
    b = f"{a: .4f}"
    return b


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


def main():
    # args = sys.argv[1:]
    # if len(args) < 2:
    # sys.exit( "NeedTwoArguments" + " <word_filename>  <answers_filename" )
    # data_filename = args[0]
    # answers_filename = args[1]
    first_guesses = [
        # 'ABUSE',
        # 'ADEPT',
        # 'ADIEU',
        # 'ALONE',
        'ALERT',
        # 'ARGUE',
        'ARISE',
        'AROSE',
        # 'AUDIO',
        # 'AULOI',
        # 'AUREI',
        # 'CAMEO',
        # 'CLAMP',
        # 'CLASP',
        # 'CLOSE',
        'CRANE',
        'CRATE',
        # 'DEPOT',
        # 'EARLY',
        # 'EASEL',
        # 'FUGUE',
        # 'GOURD',
        # 'GUIDE',
        # 'HAUTE',
        # 'HOUSE',
        # 'IMBUE',
        # 'JUICE',
        # 'KOALA',
        # 'LANCE',
        'LATER',
        # 'LEANT',
        # 'LIEGE',
        # 'LOUIE',
        # 'MAUVE',
        # 'MEDIA',
        # 'MIAOU',
        # 'MOVIE',
        # 'NAIVE',
        # 'OATER',
        # 'OCEAN',
        'ORATE',
        # 'OUIJA',
        # 'OURIE',
        # 'PALER',
        # 'PATIO',
        # 'PEARS',
        # 'PIANO',
        # 'PLAID',
        # 'POETS',
        # 'PRINT',
        # 'QUAIL',
        # 'QUIET',
        # 'QUITE',
        # 'RADIO',
        # 'RAISE',
        # 'RATIO',
        'REAST',
        # 'RECAP',
        'ROATE',
        # 'ROAST',
        'SALET',
        # 'SAUCE',
        # 'SAUTE',
        # 'SCALP',
        'SERAL',
        'SLATE',
        'SLICE',
        'SOARE',
        'STARE',
        # 'STEAM',
        # 'STRAP',
        'TALER',
        # 'TIARA',
        'TRACE',
        # 'TRAIL',
        # 'TRAIN',
        # 'TRAMP',
        # 'TRICE',
        # 'TRIED',
        # 'UNION',
        # 'URAEI',
        # 'UTILE',
        # 'VENUE',
        # 'VIDEO',
        # 'WAIVE'

    ]
    results = []
    ResultLog.write(Configuration.get_string())
    for first_guess in first_guesses:
        average = play_full_game_with_first_guess(first_guess)
        results.append([first_guess, average])
        results.sort(key=sort_function)
        print(results)
        ResultLog.write(list_list_to_str(results))


def sort_function(e):
    return e[1]


def play_full_game_with_first_guess(first_guess="ORATE"):
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
    word_count = game.answers.words
    for i in range(len(word_count)):
        server.set_answer(i + 1)
        Log.write("---Answer= " + server.answer)
        Trace.write("---Answer=" + server.answer)
        turns = run_a_game(game, server, first_guess)
        print("Answer " + server.answer + " Turns " + str(turns))
        if turns < len(turn_counts):
            turn_counts[turns - 1] += 1
        else:
            Trace.write("***Turns too many")
        total_turns += turns
    elapsed = t.stop()
    print("Elapsed time is ", elapsed)
    print("Turn counts ", list_to_str(turn_counts))
    average = total_turns / len(word_count)
    print('average ' + round_to_string(average), " first guess ", first_guess)
    Log.write("Average is " + round_to_string(average))
    Trace.write("Turn counts " + str(turn_counts))
    ResultLog.write(
        "Turn counts " + str(turn_counts) + " Average is " + round_to_string(average) + " first guess " + first_guess)
    ResultLog.write(elapsed)
    log.close()
    trace.close()
    return average


if __name__ == "__main__":
    main()
