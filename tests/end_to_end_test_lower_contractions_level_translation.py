# -*- coding: utf-8 -*-
"""
@author: Edward Middleton-Smith
"""

from context import business_objects
from business_objects.braille_proficiency_level import Braille_Proficiency_Level
from business_objects.character_braille import Character_Braille
from business_objects.translation_braille import Translation_Braille

def test_lower_contractions_level_translation():
    print('Lower Contractions Level Translation')
    translation = Translation_Braille(
        plaintext = "Be good",
        translation_proficiency_level = Braille_Proficiency_Level(3)
    )
    translation.print()

if __name__ == "__main__":
    test_lower_contractions_level_translation()
        