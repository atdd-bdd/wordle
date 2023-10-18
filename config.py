class Configuration:
    two_letter_score_weighting = .5
    position_score_weighting = .33
    not_there_score_weighting = 1
    cutoff_high_char = 95
    cutoff_two_letter = 95
    high_char_add_to_previous = True
    two_letter_add_to_previous = True
    position_add_to_previous = True
    not_there_add_to_previous = True

    @staticmethod
    def get_string():
        s = " two_letter_score_weighting= " + str(Configuration.two_letter_score_weighting)
        s+= " position_score_weighting= " + str(Configuration.position_score_weighting)
        s+= " not_there_score_weighting= " + str(Configuration.not_there_score_weighting)
        s+= " cutoff_high_char= " + str(Configuration.cutoff_high_char)
        s+= " cutoff_two_letter= "+ str(Configuration.cutoff_two_letter)
        s+= " high_char_add_to_previous= " + str(Configuration.high_char_add_to_previous)
        s+= " two_letter_add_to_previous= " + str(Configuration.two_letter_add_to_previous)
        s+= " position_add_to_previous= " + str(Configuration.position_add_to_previous)
        s+= " not_there_add_to_previous= " + str(Configuration.not_there_add_to_previous)
        return s

