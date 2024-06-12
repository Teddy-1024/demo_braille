# -*- coding: utf-8 -*-
"""
@author: Edward Middleton-Smith
"""

from character_braille import Character_Braille

import pandas as pd
from typing import Optional, List
from pydantic import BaseModel, conlist, validator
from enum import Enum
import sys
from abc import ABC, abstractmethod
from prettytable import PrettyTable


class BaseStyle(ABC):
    @abstractmethod
    def get_defaults():
        pass
    @abstractmethod
    def get_list_headings():
        pass
    @abstractmethod
    def as_row(self):
        pass
    
    def input_from_console(cls):
        options = cls.get_defaults()
        count_options = len(options)
        table_output = PrettyTable()
        table_output.field_names = ['index'] + cls.get_list_headings() 
        for index_option in range(count_options):
            option = options[index_option]
            table_output.add_row([index_option + 1] + option.as_row())
        print()
        print("Please select product configuration from below :")
        print(table_output)
        while True:
            option = str(input("Product configuration (by index):"))
            print(option + " selected")
            if option == "#!ERRORCODE!#": exit
            for index_option in range(count_options):
                if option == str(index_option + 1):
                    return options[index_option]
    
    def input_many_from_console(cls):
        selected = []
        print(f'Inputting many {cls.__name__} objects')
        print()
        while True:
            try:
                count_inputs = int(input(f'Quantity of {cls.__name__} objects to enter:'))
            except: continue
            for index_input in range(count_inputs):
                print(f'Inputting {cls.__name__} object {index_input + 1}')
                selected_new = cls.input_from_console(cls)
                selected.append(selected_new)
            break
        return selected
    
class Enum_Braille_Proficiency_Level(Enum):
    ALPHABET_PUNCTUATION = 1
    SIMPLE_WORD_AND_GROUPSIGNS = 2
    LOWER_CONTRACTIONS = 3
    def minimum():
        return min([e.value for e in Enum_Braille_Proficiency_Level])
    def maximum():
        return max([e.value for e in Enum_Braille_Proficiency_Level])
    @staticmethod
    def get_defaults():
        return [Enum_Braille_Proficiency_Level(e) for e in range(Enum_Braille_Proficiency_Level.minimum(), Enum_Braille_Proficiency_Level.maximum() + 1)]
    @staticmethod
    def get_list_headings():
        return ['Braille Proficiency Level']
    def as_row(self):
        return [self.name]
    @staticmethod
    def input_from_console():
        return BaseStyle.input_from_console(Enum_Braille_Proficiency_Level)
    @staticmethod
    def input_many_from_console():
        return BaseStyle.input_many_from_console(Enum_Braille_Proficiency_Level)

class Translation_Braille(BaseModel):
    plaintext: str
    translation_proficiency_level: Enum_Braille_Proficiency_Level
    braille_text: List[Character_Braille] = []
    search_key: Optional[str] = None

    def __init__(self, plaintext, translation_proficiency_level, braille_text=[], search_key= None):
        super().__init__(plaintext=plaintext, translation_proficiency_level=translation_proficiency_level, braille_text=braille_text, search_key=search_key)
        self.plaintext = self.plaintext.upper()
        if braille_text == []:
            self.braille_text = self.translate_text_to_Braille()
        if search_key is None:
            self.search_key = plaintext

    def __repr__(self):
        return f"{self.plaintext} - {self.translation_proficiency_level} - {self.braille_text}"
    
    def translate_text_to_Braille(self):
        known_translations = Translation_Braille.get_defaults_DataFrame()
        # delimiters = Translation_Braille.get_delimiters()
        braille_text = []
        max_key_length = known_translations.apply(lambda x: len(x[3]), axis=1).max()
        length_plaintext = len(self.plaintext)
        index_key_start = 0
        while index_key_start < length_plaintext:
            found_key = False
            for key_length in range(min(max_key_length, length_plaintext - index_key_start), 0, -1):
                key = self.plaintext[index_key_start : index_key_start + key_length]
                """if key in delimiters:
                    character_braille = Character_Braille.get_blank_Character_Braille()
                    character_braille.plaintext = delimiters[key]
                    braille_text.append(character_braille)
                    index_key_start += key_length
                    continue
                el"""
                if key == "@?NOTHING": 
                    index_key_start += key_length
                    found_key = True
                    break
                elif key == "@?NEWLINE":
                    character_braille = Character_Braille("NEWLINE", [0, 0, 0, 0, 0, 0])
                    braille_text.append(character_braille)
                    index_key_start += key_length
                    found_key = True
                    break
                if known_translations.apply(lambda x: x[3] == key and x[1].value <= self.translation_proficiency_level.value, axis=1).any():
                    translation_Braille = known_translations.apply(lambda x: x if (x[3] == key and x[1].value <= self.translation_proficiency_level.value) else None, axis=1).dropna().values.tolist()[0]
                    braille_text.append(translation_Braille[2])
                    index_key_start += key_length
                    found_key = True
                    break
            if not found_key:
                raise KeyError("Key not found starting from: ", key)
        return braille_text

    def get_delimiters():
        return {
            "@?NUM" : "NUMBER",
            "@?NOTHING" : "",
            #" " : "",
            '"@?BO' : '"', 
            '"@?BC' : '"',
            "-@?S" : "-", 
            "-@?L" : "-", 
            "/@?B" : "/", 
            "[@?BPH" : "[", 
            "]@?BPH" : "]", 
            "[@?BSQ" : "[",  
            "]@?BSQ" : "]",  
            "'@?BO" : "'",  
            "'@?BC" : "'",
            "@?LET" : "LET",
            "@?CAPS" : "CAPS",
            "@?EMPH" : "EMPH",
            "@?ABBREV1" : "ABBREV",
            "@?ABBREV2" : "ABBREV",
            "@?ABBREV3" : "ABBREV",
            "@?ABBREV4" : "ABBREV",
        }
    
    def get_defaults_DataFrame():
        df = pd.DataFrame(data=[
            ["A", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 0, 0, 0]], None], 
            ["B", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 0, 0, 0]], None], 
            ["C", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 1, 0, 0]], None], 
            ["D", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 1, 1, 0]], None],  
            ["E", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 0, 1, 0]], None],  
            ["F", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 1, 0, 0]], None],  
            ["G", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 1, 1, 0]], None],  
            ["H", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 0, 1, 0]], None], 
            ["I", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 1, 0, 0]], None], 
            ["J", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 1, 1, 0]], None],  
            ["K", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 0, 0]], None], 
            ["L", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 0, 0, 0]], None], 
            ["M", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 0, 0]], None], 
            ["N", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 1, 0]], None], 
            ["O", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 1, 0]], None], 
            ["P", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 1, 0, 0]], None], 
            ["Q", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 1, 1, 0]], None], 
            ["R", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 0, 1, 0]], None], 
            ["S", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 1, 0, 0]], None], 
            ["T", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 1, 1, 0]], None], 
            ["U", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 0, 1]], None],  
            ["V", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 0, 0, 1]], None], 
            ["W", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 1, 1, 1]], None], 
            ["X", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 0, 1]], None], 
            ["Y", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 1, 1]], None], 
            ["Z", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 1, 1]], None], 
            ['NUMBER', Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 1, 1, 1]], "@?NUM"],
            #" ", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 0]], None], 
            [",", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 0, 0, 0]], None], 
            [";", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 0]], None],  
            [":", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 0, 1, 0]], None], 
            [".", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 0, 1, 1]], None], 
            ["!", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 0]], None], 
            ["(", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1]], None], 
            [")", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1]], None], 
            ["?", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1]], None],
            ['"', Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1]], '"@?BO'], 
            ['"', Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 1, 1]], '"@?BC'],
            ["'", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 0]], None],  
            ["ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0]], "@?ABBREV1"],
            ["ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0]], "@?ABBREV2"],
            ["ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1]], "@?ABBREV3"], 
            ["ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 1, 0]], "@?ABBREV4"],  
            ["...", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0]], None],
            ["-", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1]], None], 
            ["-", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1]], "-@?S"], 
            ["-", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1]], "-@?L"], 
            ["/", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1]], "/@?B"], 
            ["\\", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1]], "\@?B"], 
            ["[", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1]], "[@?BPH"], 
            ["]", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1]], "]@?BPH"], 
            ["<", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1]], None], 
            [">", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1]], None],  
            ["/", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 0, 1, 1, 0, 0]], None], 
            ["{", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]], None], 
            ["}", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]], None], 
            ["[", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 1, 1]], "[@?BSQ"],  
            ["]", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 1]], "]@?BSQ"],  
            ["'", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 1]], "'@?BO"],  
            ["'", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 1]], "'@?BC"],
            # oldbrailledict_2 = {
            # Simple Upper Wordsigns
            ["BUT", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 0, 0]], None],
            ["CAN", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 0]], None],
            ["DO", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 0]], None],
            ["EVERY", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 0]], None],
            ["FROM", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 0, 0]], None],
            ["GO", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 1, 0]], None],
            ["HAVE", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 0]], None],
            ["JUST", Enum_Braille_Proficiency_Level(2), [[0, 1, 0, 1, 1, 0]], None],
            ["KNOWLEDGE", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 0, 0, 0]], None],
            ["LIKE", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 0, 0]], None],
            ["MORE", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 0, 0]], None],
            ["NOT", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 1, 0]], None],
            ["PEOPLE", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 0, 0]], None],
            ["QUITE", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 1, 0]], None],
            ["RATHER", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 1, 0]], None],
            ["SO", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 0, 0]], None],
            ["THAT", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 1, 0]], None],
            ["US", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 0, 0, 1]], None],
            ["VERY", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 0, 1]], None],
            ["WILL", Enum_Braille_Proficiency_Level(2), [[0, 1, 0, 1, 1, 1]], None],
            ["IT", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 0, 1]], None],
            ["YOU", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 1, 1]], None],
            ["AS", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 0, 1, 1]], None],
            ["CHILD", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 0, 1]], None],
            ["SHALL", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 1]], None],
            ["THIS", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 1]], None],
            ["WHICH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 1]], None],
            ["OUT", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 1]], None],
            ["STILL", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 0]], None],
            # Simple Upper Groupsigns
            ["AND", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 0, 1]], None],
            ["FOR", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 1, 1]], None],
            ["OF", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 1, 1]], None],
            ["THE", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 0, 1]], None],
            ["WITH", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 1, 1]], None],
            ["CH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 0, 1]], None],
            ["GH", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 0, 1]], None],
            ["SH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 1]], None],
            ["TH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 1]], None],
            ["WH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 1]], None],
            ["ED", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 0, 1]], None],
            ["ER", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 1, 1]], None],
            ["OU", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 1]], None],
            ["OW", Enum_Braille_Proficiency_Level(2), [[0, 1, 0, 1, 0, 1]], None],
            ["ST", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 0]], None],
            ["AR", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 1, 0]], None],
            ["ING", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 1]], None],
            ["BLE", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 1, 1]], None],
            # oldbrailledict_3 = {
            # Lower Contractions
            # Initial Groupsigns
            ["BE", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 0, 0]], None],
            ["COM", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 0, 1]], None],
            ["CON", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 0]], None],
            ["DIS", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 1]], None],
            # Initial-Medial-Terminal Groupsigns
            ["EN", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 1]], None],
            ["IN", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 0]], None],
            # Medial Groupsigns
            ["EA", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 0]], None],
            ["BB", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 0, 0]], None],
            ["CC", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 0]], None],
            ["DD", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 1]], None],
            ["FF", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 0]], None],
            ["GG", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 1]], None],
            # Wordsigns
            ["ENOUGH", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 1]], None],
            ["TO", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 0]], None],
            ["WERE", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0 , 1, 1]], None],
            ["HIS", Enum_Braille_Proficiency_Level(3),  [[0, 1, 1, 0, 0, 1]], None],
            ["INTO", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 0]], None], #(sequenced)
            ["BY", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 1]], None], #(sequenced)
            ["WAS", Enum_Braille_Proficiency_Level(3), [[0, 0 , 1, 0 , 1, 1]], None],
            
            # Modifiers
            ["LET", Enum_Braille_Proficiency_Level(3), [[0, 0, 0, 0, 1, 1]], "@?LET"],
            ["CAPS", Enum_Braille_Proficiency_Level(3), [[0, 0, 0, 0, 0, 1]], "@?CAPS"],
            ["EMPH", Enum_Braille_Proficiency_Level(3), [[0, 0, 0, 1, 0, 1]], "@?EMPH"],
            [" ", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 0]], "@?BLANK_SPACE"],
        ], columns=['plaintext', 'translation_proficiency_level', 'lists_dots_braille', 'search_key']) # Translation_Braille.__name__])
        df.loc[df["search_key"].isnull(), "search_key"] = df["plaintext"]
        return df
    
    @staticmethod
    def get_defaults():
        # return [Translation_Braille(plaintext, translation_proficiency_level, lists_dots_braille, search_key) for [plaintext, translation_proficiency_level, lists_dots_braille, search_key] in Translation_Braille.get_defaults_DataFrame()]
        return pd.DataFrame(data={Translation_Braille.__name__: Translation_Braille.get_defaults_DataFrame().apply(lambda x: Translation_Braille(x[0], x[1], [Character_Braille(x[0] if index_y == 0 else '', x[2][index_y]) for index_y in range(len(x[2]))], x[3]), axis=1)})
    
    @staticmethod
    def get_list_headings():
        return ['plaintext', 'translation proficiency level', 'lists dots braille', 'search key']
    
    def as_row(self):
        return [self.plaintext, self.translation_proficiency_level, self.braille_text, self.search_key]

    @staticmethod
    def input_from_console():
        print()
        print("Braille Translation Options:")
        while True:
            plaintext = str(input("Enter plaintext:"))
            if plaintext == "#!ERRORCODE!#": exit
            translation_proficiency_level = Enum_Braille_Proficiency_Level.input_from_console()
            try:
                return Translation_Braille(plaintext, translation_proficiency_level)
            except:
                pass
                
 
"""
    def get_defaults():
        return pd.DataFrame(data={Translation_Braille.__name__: [
            Character_Braille("A", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 0, 0, 0]]), 
            Character_Braille("B", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 0, 0, 0]]), 
            Character_Braille("C", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 1, 0, 0]]), 
            Character_Braille("D", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 1, 1, 0]]),  
            Character_Braille("E", Enum_Braille_Proficiency_Level(1), [[1, 0, 0, 0, 1, 0]]),  
            Character_Braille("F", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 1, 0, 0]]),  
            Character_Braille("G", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 1, 1, 0]]),  
            Character_Braille("H", Enum_Braille_Proficiency_Level(1), [[1, 1, 0, 0, 1, 0]]), 
            Character_Braille("I", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 1, 0, 0]]), 
            Character_Braille("J", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 1, 1, 0]]),  
            Character_Braille("K", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 0, 0]]), 
            Character_Braille("L", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 0, 0, 0]]), 
            Character_Braille("M", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 0, 0]]), 
            Character_Braille("N", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 1, 0]]), 
            Character_Braille("O", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 1, 0]]), 
            Character_Braille("P", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 1, 0, 0]]), 
            Character_Braille("Q", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 1, 1, 0]]), 
            Character_Braille("R", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 0, 1, 0]]), 
            Character_Braille("S", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 1, 0, 0]]), 
            Character_Braille("T", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 1, 1, 0]]), 
            Character_Braille("U", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 0, 1]]),  
            Character_Braille("V", Enum_Braille_Proficiency_Level(1), [[1, 1, 1, 0, 0, 1]]), 
            Character_Braille("W", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 1, 1, 1]]), 
            Character_Braille("X", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 0, 1]]), 
            Character_Braille("Y", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 1, 1, 1]]), 
            Character_Braille("Z", Enum_Braille_Proficiency_Level(1), [[1, 0, 1, 0, 1, 1]]), 
            Character_Braille('NUMBER', Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 1, 1, 1]], "@?NUM"),
            #" ", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 0]]), 
            Character_Braille(",", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 0, 0, 0]]), 
            Character_Braille(";", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 0]]),  
            Character_Braille(":", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 0, 1, 0]]), 
            Character_Braille(".", Enum_Braille_Proficiency_Level(1), [[0, 1, 0, 0, 1, 1]]), 
            Character_Braille("!", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 0]]), 
            Character_Braille("(", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1]]), 
            Character_Braille(")", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1]]), 
            Character_Braille("?", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1]]),
            Character_Braille('"', Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1]], '"@?BO'), 
            Character_Braille('"', Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 1, 1]], '"@?BC'),
            Character_Braille("'", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 0]]),  
            Character_Braille("ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0]], "@?ABBREV1"),
            Character_Braille("ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0]], "@?ABBREV2"),
            Character_Braille("ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1]], "@?ABBREV3"), 
            Character_Braille("ABBREV", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 1, 0]], "@?ABBREV4"),  
            Character_Braille("...", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0]]),
            Character_Braille("-", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1]]), 
            Character_Braille("-", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1]], "-@?S"), 
            Character_Braille("-", Enum_Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1]], "-@?L"), 
            Character_Braille("/", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1]], "/@?B"), 
            Character_Braille("\\", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1]], "\@?B"), 
            Character_Braille("[", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1]], "[@?BPH"), 
            Character_Braille("]", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1]], "]@?BPH"), 
            Character_Braille("<", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1]]), 
            Character_Braille(">", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1]]),  
            Character_Braille("/", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 0, 1, 1, 0, 0]]), 
            Character_Braille("{", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]]), 
            Character_Braille("}", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]]), 
            Character_Braille("[", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 1, 1]], "[@?BSQ"),  
            Character_Braille("]", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 1]], "]@?BSQ"),  
            Character_Braille("'", Enum_Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 1]], "'@?BO"),  
            Character_Braille("'", Enum_Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 1]], "'@?BC"),
            # oldbrailledict_2 = {
            # Simple Upper Wordsigns
            Character_Braille("BUT", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 0, 0]]),
            Character_Braille("CAN", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 0]]),
            Character_Braille("DO", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 0]]),
            Character_Braille("EVERY", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 0]]),
            Character_Braille("FROM", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 0, 0]]),
            Character_Braille("GO", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 1, 0]]),
            Character_Braille("HAVE", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 0]]),
            Character_Braille("JUST", Enum_Braille_Proficiency_Level(2), [[0, 1, 0, 1, 1, 0]]),
            Character_Braille("KNOWLEDGE", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 0, 0, 0]]),
            Character_Braille("LIKE", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 0, 0]]),
            Character_Braille("MORE", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 0, 0]]),
            Character_Braille("NOT", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 1, 0]]),
            Character_Braille("PEOPLE", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 0, 0]]),
            Character_Braille("QUITE", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 1, 0]]),
            Character_Braille("RATHER", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 1, 0]]),
            Character_Braille("SO", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 0, 0]]),
            Character_Braille("THAT", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 1, 0]]),
            Character_Braille("US", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 0, 0, 1]]),
            Character_Braille("VERY", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 0, 1]]),
            Character_Braille("WILL", Enum_Braille_Proficiency_Level(2), [[0, 1, 0, 1, 1, 1]]),
            Character_Braille("IT", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 0, 1]]),
            Character_Braille("YOU", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 1, 1, 1]]),
            Character_Braille("AS", Enum_Braille_Proficiency_Level(2), [[1, 0, 1, 0, 1, 1]]),
            Character_Braille("CHILD", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 0, 1]]),
            Character_Braille("SHALL", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 1]]),
            Character_Braille("THIS", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 1]]),
            Character_Braille("WHICH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 1]]),
            Character_Braille("OUT", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 1]]),
            Character_Braille("STILL", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 0]]),
            # Simple Upper Groupsigns
            Character_Braille("AND", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 0, 1]]),
            Character_Braille("FOR", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 1, 1, 1]]),
            Character_Braille("OF", Enum_Braille_Proficiency_Level(2), [[1, 1, 1, 0, 1, 1]]),
            Character_Braille("THE", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 0, 1]]),
            Character_Braille("WITH", Enum_Braille_Proficiency_Level(2), [[0, 1, 1, 1, 1, 1]]),
            Character_Braille("CH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 0, 1]]),
            Character_Braille("GH", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 0, 1]]),
            Character_Braille("SH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 1]]),
            Character_Braille("TH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 1]]),
            Character_Braille("WH", Enum_Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 1]]),
            Character_Braille("ED", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 0, 1]]),
            Character_Braille("ER", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 1, 1, 1]]),
            Character_Braille("OU", Enum_Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 1]]),
            Character_Braille("OW", Enum_Braille_Proficiency_Level(2), [[0, 1, 0, 1, 0, 1]]),
            Character_Braille("ST", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 0]]),
            Character_Braille("AR", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 1, 0]]),
            Character_Braille("ING", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 1]]),
            Character_Braille("BLE", Enum_Braille_Proficiency_Level(2), [[0, 0, 1, 1, 1, 1]]),
            # oldbrailledict_3 = {
            # Lower Contractions
            # Initial Groupsigns
            Character_Braille("BE", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 0, 0]]),
            Character_Braille("COM", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 0, 1]]),
            Character_Braille("CON", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 0]]),
            Character_Braille("DIS", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 1]]),
            # Initial-Medial-Terminal Groupsigns
            Character_Braille("EN", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 1]]),
            Character_Braille("IN", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 0]]),
            # Medial Groupsigns
            Character_Braille("EA", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 0]]),
            Character_Braille("BB", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 0, 0]]),
            Character_Braille("CC", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 0]]),
            Character_Braille("DD", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 1]]),
            Character_Braille("FF", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 0]]),
            Character_Braille("GG", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 1]]),
            # Wordsigns
            Character_Braille("ENOUGH", Enum_Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 1]]),
            Character_Braille("TO", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 0]]),
            Character_Braille("WERE", Enum_Braille_Proficiency_Level(3), [[0, 1, 1, 0 , 1, 1]]),
            Character_Braille("HIS", Enum_Braille_Proficiency_Level(3),  [[0, 1, 1, 0, 0, 1]]),
            Character_Braille("INTO", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 0]]), #(sequenced)
            Character_Braille("BY", Enum_Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 1]]), #(sequenced)
            Character_Braille("WAS", Enum_Braille_Proficiency_Level(3), [[0, 0 , 1, 0 , 1, 1]]),
            
            # Modifiers
            Character_Braille("LET", Enum_Braille_Proficiency_Level(3), [[0, 0, 0, 0, 1, 1]], "@?LET"),
            Character_Braille("CAPS", Enum_Braille_Proficiency_Level(3), [[0, 0, 0, 0, 0, 1]], "@?CAPS"),
            Character_Braille("EMPH", Enum_Braille_Proficiency_Level(3), [[0, 0, 0, 1, 0, 1]], "@?EMPH"),
        ]}, columns=[Translation_Braille.__name__])
        # remove None 's - rejected inputs 
        valid = False
        while not valid:
            try:
                temp_dict.remove(None)
            except:
                valid = True
        braille_dict = pd.DataFrame([x.as_dict() for x in temp_dict]) # , columns=['key', 'level', 'msg', 'msg_prefix'])
    # RETURNS
        # print('Braille Dictionary Creation')
        # print(f"type(temp_dict) = {type(temp_dict)}")
        # print("temp_dict = ")
        # for i in range(len(temp_dict)):
        #     print(f"{temp_dict[i]}")
        # print('')
        # print(f"type(braille_dict) = {type(braille_dict)}")
        # print(f"braille_dict = {braille_dict}")
        
        return braille_dict # temp_dict # braille_dict
        """