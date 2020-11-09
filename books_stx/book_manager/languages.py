from iso_language_codes import language_dictionary


def get_language_codes():
    language_codes = list(language_dictionary().keys())
    language_codes.remove("")
    return language_codes
