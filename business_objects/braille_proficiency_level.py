"""
@author: Edward Middleton-Smith
Precision And Research Technology Systems Limited
"""

from business_objects.attribute_abstract import Attribute_Abstract

from enum import Enum


class Braille_Proficiency_Level(Enum):
    ALPHABET_PUNCTUATION = 1
    SIMPLE_WORD_AND_GROUPSIGNS = 2
    LOWER_CONTRACTIONS = 3
    def minimum():
        return min([e.value for e in Braille_Proficiency_Level])
    def maximum():
        return max([e.value for e in Braille_Proficiency_Level])
    @staticmethod
    def get_defaults():
        return [Braille_Proficiency_Level(e) for e in range(Braille_Proficiency_Level.minimum(), Braille_Proficiency_Level.maximum() + 1)]
    @staticmethod
    def get_list_headings():
        return ['Braille Proficiency Level']
    def as_row(self):
        return [self.name]
    @staticmethod
    def input_from_console():
        return Attribute_Abstract.input_from_console(Braille_Proficiency_Level)
    @staticmethod
    def input_many_from_console():
        return Attribute_Abstract.input_many_from_console(Braille_Proficiency_Level)