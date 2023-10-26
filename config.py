class Configuration:
    #  twowgt= 0.33 poswgt= 0.33 notwgt= 0.5 cuthig= 90 cuttwo= 90 cutpos= 90 cutnt= 90 higadd= True twoadd= True
    #  posadd= True ntadd= True repwgt= 0.1 repscr= 0 hard_mode= False===3.753  with TARSE and 1 failure
    answer_filename = "wordlist_hidden"
    data_filename = "wordlist_all"
    use_short_answer_list = False
    # answer_filename = "answers.txt"
    # data_filename= "words002.txt"
    hard_mode = False
    cutoff_high_char = 90
    cutoff_two_letter = 90
    cutoff_not_there = 90
    cutoff_position = 90
    high_char_add_to_previous = True
    two_letter_add_to_previous = True
    position_add_to_previous = True
    not_there_add_to_previous = True
    two_letter_score_weighting = .33
    position_score_weighting = .33
    not_there_score_weighting = .5
    minimum_to_filter = 50
    repeated_char_weighting = .1  # Seems to not be needed
    repeated_char_scoring = 0  # check this out - seems to get worse
    trace_output = True
    log_output = True
    trace_detail = False
    first_word = "TARSE"

    @staticmethod
    def get_files():
        return "Data file " + Configuration.data_filename + " answer file " + Configuration.answer_filename

    @staticmethod
    def get_string():
        s = " two_letter_score_weighting= " + str(Configuration.two_letter_score_weighting)
        s += " position_score_weighting= " + str(Configuration.position_score_weighting)
        s += " not_there_score_weighting= " + str(Configuration.not_there_score_weighting)
        s += " cutoff_high_char= " + str(Configuration.cutoff_high_char)
        s += " cutoff_two_letter= " + str(Configuration.cutoff_two_letter)
        s += " cutoff_position= " + str(Configuration.cutoff_position)
        s += " cutoff_not_there= " + str(Configuration.cutoff_not_there)
        s += " high_char_add_to_previous= " + str(Configuration.high_char_add_to_previous)
        s += " two_letter_add_to_previous= " + str(Configuration.two_letter_add_to_previous)
        s += " position_add_to_previous= " + str(Configuration.position_add_to_previous)
        s += " not_there_add_to_previous= " + str(Configuration.not_there_add_to_previous)
        s += " repeated_char_weighting= " + str(Configuration.repeated_char_weighting)
        s += " repeated_char_scoring= " + str(Configuration.repeated_char_scoring)
        s += " hard_mode= " + str(Configuration.hard_mode)

        return s

    @classmethod
    def get_short_string(cls):
        s = " twowgt= " + str(Configuration.two_letter_score_weighting)
        s += " poswgt= " + str(Configuration.position_score_weighting)
        s += " notwgt= " + str(Configuration.not_there_score_weighting)
        s += " cuthig= " + str(Configuration.cutoff_high_char)
        s += " cuttwo= " + str(Configuration.cutoff_two_letter)
        s += " cutpos= " + str(Configuration.cutoff_position)
        s += " cutnt= " + str(Configuration.cutoff_not_there)
        s += " higadd= " + str(Configuration.high_char_add_to_previous)
        s += " twoadd= " + str(Configuration.two_letter_add_to_previous)
        s += " posadd= " + str(Configuration.position_add_to_previous)
        s += " ntadd= " + str(Configuration.not_there_add_to_previous)
        s += " repwgt= " + str(Configuration.repeated_char_weighting)
        s += " repscr= " + str(Configuration.repeated_char_scoring)
        s += " hard_mode= " + str(Configuration.hard_mode)
        return s
