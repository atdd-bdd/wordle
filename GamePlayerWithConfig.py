from Log import *
from OneGamePlayer import play_full_game_with_first_guess
from game_helper import play_partial_game_with_first_guess
from server import *


def main():
    log = Log("log_GamePlayerWithConfig.txt")
    trace = Trace("trace_GamePlayerWithConfig.txt")
    Configuration.log_output = False
    # Configuration.trace_output = False
    Configuration.use_short_answer_list = False
    ResultLog.write("----Game with Configuration Player End  " + Configuration.get_files())
    ResultLog.write(Configuration.get_string())
    results = []
    results_solved_all = []
    for Configuration.position_add_to_previous in [True]:
        for Configuration.high_char_add_to_previous in [True]:
            for Configuration.not_there_add_to_previous in [True]:
                for Configuration.two_letter_add_to_previous in [True]:
                    for Configuration.cutoff_not_there in [90, 50]:
                        for Configuration.cutoff_high_char in [90, 50]:
                            for Configuration.cutoff_position in [90, 50]:
                                for Configuration.cutoff_two_letter in [90, 50]:
                                    for Configuration.not_there_score_weighting in [.5, 1]:
                                        for Configuration.position_score_weighting in [1.0, .66, .33]:
                                            for Configuration.two_letter_score_weighting in [1.0, .66, .33]:
                                                for Configuration.repeated_char_weighting in [.1]:
                                                    # print(Configuration.get_string())
                                                    print(Configuration.get_short_string())
                                                    Trace.write(Configuration.get_string())
                                                    average, turn_counts = play_game_for_various_starting_words()
                                                    print(" Results average= ", average, " turn_counts= ", turn_counts)
                                                    if turn_counts[6] == 0:
                                                        print("**** Solved all ")
                                                        # ResultLog.write("**** Solved all")
                                                        results_solved_all.append(
                                                            [Configuration.get_short_string() + "==", average])
                                                    results.append([Configuration.get_short_string() + "==", average])
                                                    # results.sort(key=sort_function)
                                                    ResultLog.write(Configuration.get_short_string())
                                                    ResultLog.write(" Turn counts " + list_to_str(turn_counts) + average)
                                                    # ResultLog.write(list_list_to_str(results))
                                                    # print(list_list_to_str(results))
    log.close()
    trace.close()
    ResultLog.write(list_list_to_str(results))
    results.sort(key=sort_function)
    ResultLog.write(list_list_to_str(results))
    ResultLog.write("Solved all " + list_list_to_str(results_solved_all))
    results_solved_all.sort(key=sort_function)
    ResultLog.write(list_list_to_str(results_solved_all))
    ResultLog.write("----Game with Configuration Player End " + Configuration.get_files())
    print(list_list_to_str(results))


def play_game_for_various_starting_words(results=None):
    if results is None:
        results = [Configuration.first_word]
    average = 0
    turn_counts = []
    for first_guess in results:
        if Configuration.use_short_answer_list:
            average, turn_counts = play_partial_game_with_first_guess(first_guess)
        else:
            average, turn_counts = play_full_game_with_first_guess(first_guess)
    return average, turn_counts


if __name__ == "__main__":
    main()
