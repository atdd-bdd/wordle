from Log import *
from game_helper import play_full_game_with_first_guess
from server import *


def main():
    log = Log("log_OneGamePlayer.txt")
    trace = Trace("trace_OneGamePlayer.txt")
    ResultLog.write(Configuration.get_string())
    ResultLog.write(Configuration.get_files())
    ResultLog.write("----One Game Player Start " + Configuration.get_files())
    results = []
    for first_guess in ["", "CRATE"]:
        average = play_full_game_with_first_guess(first_guess)
        results.append([first_guess, average])
        results.sort(key=sort_function)
        print(results)
        ResultLog.write(list_list_to_str(results))
    ResultLog.write("----One Game Player End " + Configuration.get_files())
    log.close()
    trace.close()


if __name__ == "__main__":
    main()
