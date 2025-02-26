# -*- coding: utf-8 -*-
"""
@author: Edward Middleton-Smith
"""

from end_to_end_test_alphabet_level_translation import test_alphabet_level_translation
from end_to_end_test_simple_word_and_groupsigns_level_translation import test_simple_words_and_groupsigns_level_translation
from end_to_end_test_lower_contractions_level_translation import test_lower_contractions_level_translation
from integration_test_get_all_characters import test_get_all_characters


if __name__ == "__main__":
    # Integration test
    test_get_all_characters()
    # End to end tests
    test_alphabet_level_translation()
    test_simple_words_and_groupsigns_level_translation()
    test_lower_contractions_level_translation()
        