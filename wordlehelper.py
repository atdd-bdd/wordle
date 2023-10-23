from GameRound import *


def main():
    args = sys.argv[1:]
    data_filename = Configuration.data_filename
    answers_filename = Configuration.answer_filename
    print("Using " + Configuration.get_files())
    trace = Trace("trace_word_helper.txt")
    Trace.write(Configuration.get_files())
    log = Log("log_word_helper.txt")
    game = GameRound(data_filename, answers_filename)
    guesses = []
    matches = []
    guess = game.get_guess(guesses, matches)
    Trace.write("initial " + guess)
    print("Guess could be: ", guess)
    for i in range(6):
        guess, match = input_guess_match()
        if match == "EEEEE":
            break
        guesses.append(guess)
        matches.append(match)
        guess = game.get_guess(guesses, matches)
        print("Guess could be ", guess)
    log.close()
    trace.close()


def input_guess_match():
    good = False
    guess = ""
    match = ""
    while not good:
        inp = input("Guess result: ").upper()
        print(inp)
        if ' ' in inp:
            guess, match = inp.split(' ')
            if len(guess) == 5 and len(match) == 5:
                good = True
        if not good:
            print("Invalid entry: ")
    return guess, match


if __name__ == "__main__":
    main()
