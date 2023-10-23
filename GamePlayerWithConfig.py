from Log import *
from OneGamePlayer import play_full_game_with_first_guess
from game_helper import play_partial_game_with_first_guess
from server import *


def main():
    log = Log("log_GamePlayerWithConfig.txt")
    trace = Trace("trace_GamePlayerWithConfig.txt")
    Configuration.log_output = False
    # Configuration.trace_output = False
    Configuration.use_short_answer_list = True
    ResultLog.write("----Game with Configuration Player End  " + Configuration.get_files())
    ResultLog.write(Configuration.get_string())
    results = []
    for Configuration.position_add_to_previous in [True]:
        for Configuration.high_char_add_to_previous in [True]:
            for Configuration.not_there_add_to_previous in [False, True]:
                for Configuration.two_letter_add_to_previous in [True]:
                    for Configuration.cutoff_not_there in [50, 90]:
                        for Configuration.cutoff_high_char in [50, 90]:
                            for Configuration.cutoff_position in [50, 90]:
                                for Configuration.cutoff_two_letter in [50, 90]:
                                    for Configuration.not_there_score_weighting in [1]:
                                        for Configuration.position_score_weighting in [.66]:
                                            for Configuration.two_letter_score_weighting in [.66]:
                                                for Configuration.repeated_char_weighting in [0., .2, ]:
                                                    print(Configuration.get_string())
                                                    print(Configuration.get_short_string())
                                                    Trace.write(Configuration.get_string())
                                                    average = play_game_for_various_starting_words()
                                                    results.append([Configuration.get_short_string(), average])
                                                    results.sort(reverse=True, key=sort_function)
                                                    ResultLog.write(Configuration.get_short_string())
                                                    ResultLog.write(list_list_to_str(results))
                                                    print(list_list_to_str(results))
    log.close()
    trace.close()
    ResultLog.write(list_list_to_str(results))
    results.sort(reverse=True, key=sort_function)
    ResultLog.write(list_list_to_str(results))
    ResultLog.write("----Game with Configuration Player End " + Configuration.get_files())
    print(list_list_to_str(results))


def play_game_for_various_starting_words(results=None):
    if results is None:
        results = ["SARED"]
    average = 0
    for first_guess in results:
        if Configuration.use_short_answer_list:
            average = play_partial_game_with_first_guess(first_guess)
        else:
            average = play_full_game_with_first_guess(first_guess)
    return average


if __name__ == "__main__":
    main()
