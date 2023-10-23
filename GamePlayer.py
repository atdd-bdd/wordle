from Log import *
from OneGamePlayer import play_full_game_with_first_guess
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
        'ARIAL',
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
    for first_guess in first_guesses:
        average = play_full_game_with_first_guess(first_guess)
        results.append([first_guess, average])
        results.sort(key=sort_function)
        print(results)
        ResultLog.write(list_list_to_str(results))
    ResultLog.write("----Game Player End " + Configuration.get_files())
    log.close()
    trace.close()


if __name__ == "__main__":
    main()
