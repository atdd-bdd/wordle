from GamePlayer import run_a_game, round_to_string
from GameRound import *
from server import *
from Log import *
from timer import Timer


def main():
    results = []
    for first_guess in ["", "CRATE"]:
        average = play_full_game_with_first_guess(first_guess)
        results.append([first_guess, average])
        results.sort(key=sort_function)
        print(results)
        ResultLog.write(list_list_to_str(results))


def play_full_game_with_first_guess(first_guess=""):
    log = Log("log_OneGamePlayer.txt")
    trace = Trace("trace_OneGamePlayer.txt")
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
    log.close()
    trace.close()
    return average


if __name__ == "__main__":
    main()
