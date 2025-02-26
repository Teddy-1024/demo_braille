# -*- coding: utf-8 -*-
"""
@author: Edward Middleton-Smith
"""

from context import business_objects
from business_objects.character_braille import Character_Braille
from business_objects.translation_braille import Translation_Braille

if __name__ == "__main__":
    braille_translations = Translation_Braille.get_defaults()
    for braille_translation_row in braille_translations.iterrows():
        braille_translation_series = braille_translation_row[1]
        plaintext = braille_translation_series.iloc[0]
        translation_proficiency_level = braille_translation_series.iloc[1]
        braille_text = braille_translation_series.iloc[2]

        braille_characters = [Character_Braille(plaintext = plaintext, list_dots_braille = list_dots) for list_dots in braille_text]

        braille_translation = Translation_Braille(plaintext = plaintext, translation_proficiency_level = translation_proficiency_level, braille_text = braille_characters)
        braille_translation.print()
        