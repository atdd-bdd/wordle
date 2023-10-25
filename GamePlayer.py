from Log import *
from OneGamePlayer import play_full_game_with_first_guess
from game_helper import play_partial_game_with_first_guess
from server import *


def main():
    log = Log("log_GamePlayer.txt")
    trace = Trace("trace_GamePlayer.txt")
    first_guesses = [
        'ABUSE',
        'ADEPT',
        'ADIEU',
        'ALONE',
        'ALERT',
        'ARGUE',
        'ARIEL',
        'ARISE',
        'AROSE',
        'AUDIO',
        'AULOI',
        'AUREI',
        'CAMEO',
        'CARLE',
        'CARTE',
        'CARSE',
        'CLAMP',
        'CLASP',
        'CLOSE',
        'CRANE',
        'CRATE',
        'DEPOT',
        'DOILT',
        'EARLY',
        'EASEL',
        'FUGUE',
        'GOURD',
        'GUIDE',
        'HAUTE',
        'HOUSE',
        'IMBUE',
        'JUICE',
        'KALES',
        'KOALA',
        'LAKES',
        'LANCE',
        'LANTS',
        'LATER',
        'LEANT',
        'LIEGE',
        'LOUIE',
        'MAUVE',
        'MEDIA',
        'MIAOU',
        'MOVIE',
        'NAIVE',
        'OATER',
        'OCEAN',
        'ORATE',
        'OUIJA',
        'OURIE',
        'PALER',
        'PALET',
        'PATIO',
        'PEARS',
        'PIANO',
        'PLAID',
        'POETS',
        'PRINT',
        'QUAIL',
        'QUIET',
        'QUITE',
        'RADIO',
        'RAINE',
        'RAISE',
        'RAILE',
        'RATIO',
        'REAST',
        'RECAP',
        'ROATE',
        'ROAST',
        'SALET',
        'SAUCE',
        'SAUTE',
        'SCALP',
        'SERAL',
        'SLATE',
        'SLICE',
        'SOARE',
        'STARE',
        'STEAM',
        'STRAP',
        'TALER',
        'TARED',
        'TARSE',
        'TIARA',
        'TORSE',
        'TRACE',
        'TRAIL',
        'TRAIN',
        'TRAMP',
        'TRICE',
        'TRIED',
        'THUMP',
        'UNION',
        'URAEI',
        'UTILE',
        'VENUE',
        'VIDEO',
        'WAIVE'

    ]
    ResultLog.write(Configuration.get_string())
    ResultLog.write("----Game Player Start " + Configuration.get_files())
    results = []
    results_with_all_solved = []
    for first_guess in first_guesses:
        if Configuration.use_short_answer_list:
            average, turn_counts = play_partial_game_with_first_guess(first_guess)
        else:
            average, turn_counts = play_full_game_with_first_guess(first_guess)
        if turn_counts[6] == 0:
            print("**** Solved all ")
            ResultLog.write("**** Solved all")
            results_with_all_solved.append([first_guess, average])
            results_with_all_solved.sort(key=sort_function)
            print("Solved all ", results_with_all_solved)
        else:
            print("Did not solve all ", turn_counts)
            ResultLog.write("Did not solve all " + list_to_str(turn_counts))
        results.append([first_guess, average])
        results.sort(key=sort_function)
        print(results)
    ResultLog.write(list_list_to_str(results))
    results_with_all_solved.sort(key=sort_function)
    ResultLog.write("Solved all " + list_list_to_str(results_with_all_solved))
    good_words = [item[0] for item in results_with_all_solved]
    ResultLog.write("Good words " + list_to_str(good_words))
    print("Good words ", good_words)
    ResultLog.write("----Game Player End " + Configuration.get_files())
    log.close()
    trace.close()


if __name__ == "__main__":
    main()
