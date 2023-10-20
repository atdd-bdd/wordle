from GamePlayer import run_a_game, round_to_string
from GameRound import *
from server import *
from Log import *
from timer import Timer


def main():
    log = Log("log_GamePlayerWithConfig.txt")
    trace = Trace("trace_GamePlayerWithConfig.txt")
    Configuration.log_output = False
    Configuration.trace_output = False
    results = []
    for Configuration.position_add_to_previous in [True, False]:
        for Configuration.high_char_add_to_previous in [True, False]:
            for Configuration.not_there_add_to_previous in [True, False]:
                for Configuration.two_letter_add_to_previous in [True, False]:
                    for Configuration.cutoff_not_there in [90, 95]:
                        for Configuration.cutoff_high_char in [90,95]:
                            for Configuration.cutoff_position in [90,95]:
                                for Configuration.cutoff_two_letter in [90,95]:
                                    for Configuration.not_there_score_weighting in [1,2]:
                                        for Configuration.position_score_weighting in [.33, .66]:
                                            for Configuration.two_letter_score_weighting in [.33, .66]:
                                                print(Configuration.get_string())
                                                print(Configuration.get_short_string())
                                                Trace.write(Configuration.get_string())
                                                average = play_game_for_various_starting_words(results)
                                                results.append([Configuration.get_short_string(), average])
                                                results.sort(reverse=True, key=sort_function)
                                                ResultLog.write(list_list_to_str(results))
                                                print(list_list_to_str(results))
    log.close()
    trace.close()
    ResultLog.write(list_list_to_str(results))
    results.sort(reverse=True,key=sort_function)
    ResultLog.write(list_list_to_str(results))
    print(list_list_to_str(results))
def play_game_for_various_starting_words(results):
    for first_guess in ["CRATE"]:
        average = play_full_game_with_first_guess(first_guess)
    return average

def play_full_game_with_first_guess(first_guess=""):

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
        if i > 10:
            break
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


if __name__ == "__main__":
    main()
