def get_short_word_list():
    short_words = {'FOCAL': 4, 'LOCAL': 4, 'STATE': 5, 'STEAK': 3, 'TEASE': 3, 'VOCAL': 4, 'YEAST': 4, 'LEAST': 3,
                   'STAVE': 5,
                   'TRUSS': 3, 'TRUST': 4, 'CRUST': 3, 'SWEAT': 5, 'POUND': 4, 'PRIZE': 4, 'SHAVE': 4, 'SHARE': 3,
                   'SNARE': 3,
                   'SPARE': 3, 'TAUNT': 6, 'JAUNT': 5, 'HAUNT': 5, 'GAUNT': 5, 'VAUNT': 5, 'WATCH': 5, 'WIGHT': 5,
                   'WINCH': 5,
                   'WOUND': 5, 'GRAZE': 6, 'SNAIL': 4, 'SKUNK': 4, 'STEER': 4, 'ESTER': 3, 'RESET': 3, 'TONIC': 4,
                   'GEESE': 4,
                   'ERROR': 3, 'FEMME': 4, 'FREER': 5,
                   'TETRA': 5, 'TATER': 6, 'FAXED': 5, 'EARED': 5, 'MOOED': 7, 'TEMPO':4,
                   'OOZED':4, 'RAZED':4, 'WAXED':4, 'DARED':4, 'FAZED':4}
    sorted_list = [word for word, count in short_words.items()]
    return sorted_list


def main():
    get_short_word_list()


if __name__ == '__main__':
    main()
