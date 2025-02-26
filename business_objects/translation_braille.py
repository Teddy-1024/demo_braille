"""
@author: Edward Middleton-Smith
Precision And Research Technology Systems Limited
"""

from business_objects.character_braille import Character_Braille
# from business_objects.attribute_abstract import Attribute_Abstract
from business_objects.braille_proficiency_level import Braille_Proficiency_Level

import pandas as pd
from typing import Optional, List, ClassVar
from pydantic import BaseModel



class Translation_Braille(BaseModel):
    DF_COLUMNS: ClassVar = ['plaintext', 'translation_proficiency_level', 'lists_dots_braille', 'search_key']
    plaintext: str
    translation_proficiency_level: Braille_Proficiency_Level
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
        max_key_length = known_translations.apply(lambda x: len(x.iloc[3]), axis=1).max()
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
                if known_translations.apply(lambda x: x.iloc[3] == key and x.iloc[1].value <= self.translation_proficiency_level.value, axis=1).any():
                    translation_Braille = known_translations.apply(lambda x: x if (x.iloc[3] == key and x.iloc[1].value <= self.translation_proficiency_level.value) else None, axis=1).dropna().values.tolist()[0]
                    braille_text.append(translation_Braille.iloc[2])
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
            ["A", Braille_Proficiency_Level(1), [[1, 0, 0, 0, 0, 0]], None], 
            ["B", Braille_Proficiency_Level(1), [[1, 1, 0, 0, 0, 0]], None], 
            ["C", Braille_Proficiency_Level(1), [[1, 0, 0, 1, 0, 0]], None], 
            ["D", Braille_Proficiency_Level(1), [[1, 0, 0, 1, 1, 0]], None],  
            ["E", Braille_Proficiency_Level(1), [[1, 0, 0, 0, 1, 0]], None],  
            ["F", Braille_Proficiency_Level(1), [[1, 1, 0, 1, 0, 0]], None],  
            ["G", Braille_Proficiency_Level(1), [[1, 1, 0, 1, 1, 0]], None],  
            ["H", Braille_Proficiency_Level(1), [[1, 1, 0, 0, 1, 0]], None], 
            ["I", Braille_Proficiency_Level(1), [[0, 1, 0, 1, 0, 0]], None], 
            ["J", Braille_Proficiency_Level(1), [[0, 1, 0, 1, 1, 0]], None],  
            ["K", Braille_Proficiency_Level(1), [[1, 0, 1, 0, 0, 0]], None], 
            ["L", Braille_Proficiency_Level(1), [[1, 1, 1, 0, 0, 0]], None], 
            ["M", Braille_Proficiency_Level(1), [[1, 0, 1, 1, 0, 0]], None], 
            ["N", Braille_Proficiency_Level(1), [[1, 0, 1, 1, 1, 0]], None], 
            ["O", Braille_Proficiency_Level(1), [[1, 0, 1, 0, 1, 0]], None], 
            ["P", Braille_Proficiency_Level(1), [[1, 1, 1, 1, 0, 0]], None], 
            ["Q", Braille_Proficiency_Level(1), [[1, 1, 1, 1, 1, 0]], None], 
            ["R", Braille_Proficiency_Level(1), [[1, 1, 1, 0, 1, 0]], None], 
            ["S", Braille_Proficiency_Level(1), [[0, 1, 1, 1, 0, 0]], None], 
            ["T", Braille_Proficiency_Level(1), [[0, 1, 1, 1, 1, 0]], None], 
            ["U", Braille_Proficiency_Level(1), [[1, 0, 1, 0, 0, 1]], None],  
            ["V", Braille_Proficiency_Level(1), [[1, 1, 1, 0, 0, 1]], None], 
            ["W", Braille_Proficiency_Level(1), [[0, 1, 0, 1, 1, 1]], None], 
            ["X", Braille_Proficiency_Level(1), [[1, 0, 1, 1, 0, 1]], None], 
            ["Y", Braille_Proficiency_Level(1), [[1, 0, 1, 1, 1, 1]], None], 
            ["Z", Braille_Proficiency_Level(1), [[1, 0, 1, 0, 1, 1]], None], 
            ['NUMBER', Braille_Proficiency_Level(1), [[0, 0, 1, 1, 1, 1]], "@?NUM"],
            #" ", Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 0]], None], 
            [",", Braille_Proficiency_Level(1), [[0, 1, 0, 0, 0, 0]], None], 
            [";", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 0]], None],  
            [":", Braille_Proficiency_Level(1), [[0, 1, 0, 0, 1, 0]], None], 
            [".", Braille_Proficiency_Level(1), [[0, 1, 0, 0, 1, 1]], None], 
            ["!", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 0]], None], 
            ["(", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1]], None], 
            [")", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1]], None], 
            ["?", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1]], None],
            ['"', Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1]], '"@?BO'], 
            ['"', Braille_Proficiency_Level(1), [[0, 0, 1, 0, 1, 1]], '"@?BC'],
            ["'", Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 0]], None],  
            ["ABBREV", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0]], "@?ABBREV1"],
            ["ABBREV", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0]], "@?ABBREV2"],
            ["ABBREV", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1]], "@?ABBREV3"], 
            ["ABBREV", Braille_Proficiency_Level(1), [[0, 0, 0, 0, 1, 0]], "@?ABBREV4"],  
            ["...", Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0]], None],
            ["-", Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1]], None], 
            ["-", Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1]], "-@?S"], 
            ["-", Braille_Proficiency_Level(1), [[0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1]], "-@?L"], 
            ["/", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1]], "/@?B"], 
            ["\\", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 1]], "\\@?B"], 
            ["[", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1]], "[@?BPH"], 
            ["]", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1]], "]@?BPH"], 
            ["<", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1]], None], 
            [">", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 1, 1, 0, 1, 1]], None],  
            ["/", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 1, 1], [0, 0, 1, 1, 0, 0]], None], 
            ["{", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]], None], 
            ["}", Braille_Proficiency_Level(1), [[0, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1]], None], 
            ["[", Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 1, 1]], "[@?BSQ"],  
            ["]", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 1]], "]@?BSQ"],  
            ["'", Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 1]], "'@?BO"],  
            ["'", Braille_Proficiency_Level(1), [[0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 1]], "'@?BC"],
            # oldbrailledict_2 = {
            # Simple Upper Wordsigns
            ["BUT", Braille_Proficiency_Level(2), [[1, 1, 0, 0, 0, 0]], None],
            ["CAN", Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 0]], None],
            ["DO", Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 0]], None],
            ["EVERY", Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 0]], None],
            ["FROM", Braille_Proficiency_Level(2), [[1, 1, 0, 1, 0, 0]], None],
            ["GO", Braille_Proficiency_Level(2), [[1, 1, 0, 1, 1, 0]], None],
            ["HAVE", Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 0]], None],
            ["JUST", Braille_Proficiency_Level(2), [[0, 1, 0, 1, 1, 0]], None],
            ["KNOWLEDGE", Braille_Proficiency_Level(2), [[1, 0, 1, 0, 0, 0]], None],
            ["LIKE", Braille_Proficiency_Level(2), [[1, 1, 1, 0, 0, 0]], None],
            ["MORE", Braille_Proficiency_Level(2), [[1, 0, 1, 1, 0, 0]], None],
            ["NOT", Braille_Proficiency_Level(2), [[1, 0, 1, 1, 1, 0]], None],
            ["PEOPLE", Braille_Proficiency_Level(2), [[1, 1, 1, 1, 0, 0]], None],
            ["QUITE", Braille_Proficiency_Level(2), [[1, 1, 1, 1, 1, 0]], None],
            ["RATHER", Braille_Proficiency_Level(2), [[1, 1, 1, 0, 1, 0]], None],
            ["SO", Braille_Proficiency_Level(2), [[0, 1, 1, 1, 0, 0]], None],
            ["THAT", Braille_Proficiency_Level(2), [[0, 1, 1, 1, 1, 0]], None],
            ["US", Braille_Proficiency_Level(2), [[1, 0, 1, 0, 0, 1]], None],
            ["VERY", Braille_Proficiency_Level(2), [[1, 1, 1, 0, 0, 1]], None],
            ["WILL", Braille_Proficiency_Level(2), [[0, 1, 0, 1, 1, 1]], None],
            ["IT", Braille_Proficiency_Level(2), [[1, 0, 1, 1, 0, 1]], None],
            ["YOU", Braille_Proficiency_Level(2), [[1, 0, 1, 1, 1, 1]], None],
            ["AS", Braille_Proficiency_Level(2), [[1, 0, 1, 0, 1, 1]], None],
            ["CHILD", Braille_Proficiency_Level(2), [[1, 0, 0, 0, 0, 1]], None],
            ["SHALL", Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 1]], None],
            ["THIS", Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 1]], None],
            ["WHICH", Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 1]], None],
            ["OUT", Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 1]], None],
            ["STILL", Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 0]], None],
            # Simple Upper Groupsigns
            ["AND", Braille_Proficiency_Level(2), [[1, 1, 1, 1, 0, 1]], None],
            ["FOR", Braille_Proficiency_Level(2), [[1, 1, 1, 1, 1, 1]], None],
            ["OF", Braille_Proficiency_Level(2), [[1, 1, 1, 0, 1, 1]], None],
            ["THE", Braille_Proficiency_Level(2), [[0, 1, 1, 1, 0, 1]], None],
            ["WITH", Braille_Proficiency_Level(2), [[0, 1, 1, 1, 1, 1]], None],
            ["CH", Braille_Proficiency_Level(2), [[1, 0, 0, 0, 0, 1]], None],
            ["GH", Braille_Proficiency_Level(2), [[1, 1, 0, 0, 0, 1]], None],
            ["SH", Braille_Proficiency_Level(2), [[1, 0, 0, 1, 0, 1]], None],
            ["TH", Braille_Proficiency_Level(2), [[1, 0, 0, 1, 1, 1]], None],
            ["WH", Braille_Proficiency_Level(2), [[1, 0, 0, 0, 1, 1]], None],
            ["ED", Braille_Proficiency_Level(2), [[1, 1, 0, 1, 0, 1]], None],
            ["ER", Braille_Proficiency_Level(2), [[1, 1, 0, 1, 1, 1]], None],
            ["OU", Braille_Proficiency_Level(2), [[1, 1, 0, 0, 1, 1]], None],
            ["OW", Braille_Proficiency_Level(2), [[0, 1, 0, 1, 0, 1]], None],
            ["ST", Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 0]], None],
            ["AR", Braille_Proficiency_Level(2), [[0, 0, 1, 1, 1, 0]], None],
            ["ING", Braille_Proficiency_Level(2), [[0, 0, 1, 1, 0, 1]], None],
            ["BLE", Braille_Proficiency_Level(2), [[0, 0, 1, 1, 1, 1]], None],
            # oldbrailledict_3 = {
            # Lower Contractions
            # Initial Groupsigns
            ["BE", Braille_Proficiency_Level(3), [[0, 1, 1, 0, 0, 0]], None],
            ["COM", Braille_Proficiency_Level(3), [[0, 0, 1, 0, 0, 1]], None],
            ["CON", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 0]], None],
            ["DIS", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 1]], None],
            # Initial-Medial-Terminal Groupsigns
            ["EN", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 1]], None],
            ["IN", Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 0]], None],
            # Medial Groupsigns
            ["EA", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 0]], None],
            ["BB", Braille_Proficiency_Level(3), [[0, 1, 1, 0, 0, 0]], None],
            ["CC", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 0]], None],
            ["DD", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 1, 1]], None],
            ["FF", Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 0]], None],
            ["GG", Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 1]], None],
            # Wordsigns
            ["ENOUGH", Braille_Proficiency_Level(3), [[0, 1, 0, 0, 0, 1]], None],
            ["TO", Braille_Proficiency_Level(3), [[0, 1, 1, 0, 1, 0]], None],
            ["WERE", Braille_Proficiency_Level(3), [[0, 1, 1, 0 , 1, 1]], None],
            ["HIS", Braille_Proficiency_Level(3),  [[0, 1, 1, 0, 0, 1]], None],
            ["INTO", Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 0]], None], #(sequenced)
            ["BY", Braille_Proficiency_Level(3), [[0, 0, 1, 0, 1, 1]], None], #(sequenced)
            ["WAS", Braille_Proficiency_Level(3), [[0, 0 , 1, 0 , 1, 1]], None],
            
            # Modifiers
            ["LET", Braille_Proficiency_Level(3), [[0, 0, 0, 0, 1, 1]], "@?LET"],
            ["CAPS", Braille_Proficiency_Level(3), [[0, 0, 0, 0, 0, 1]], "@?CAPS"],
            ["EMPH", Braille_Proficiency_Level(3), [[0, 0, 0, 1, 0, 1]], "@?EMPH"],
            [" ", Braille_Proficiency_Level(1), [[0, 0, 0, 0, 0, 0]], "@?BLANK_SPACE"],
        ], columns=Translation_Braille.DF_COLUMNS) # Translation_Braille.__name__])
        df.loc[df["search_key"].isnull(), "search_key"] = df["plaintext"]
        return df
    
    @staticmethod
    def get_defaults():
        defaults_dataframe = Translation_Braille.get_defaults_DataFrame()
        return defaults_dataframe # pd.DataFrame(data={Translation_Braille.__name__: defaults_dataframe.apply(lambda x: Translation_Braille(x.iloc[0], x.iloc[1], [Character_Braille(x.iloc[0] if index_y == 0 else '', x.iloc[2][index_y]) for index_y in range(len(x.iloc[2]))], x.iloc[3]), axis=1)})
    
    @staticmethod
    def get_list_headings():
        return [str.replace(heading, '_', ' ') for heading in Translation_Braille.DF_COLUMNS]
    
    def as_row(self):
        return [self.plaintext, self.translation_proficiency_level, self.braille_text, self.search_key]

    @staticmethod
    def input_from_console():
        print()
        print("Braille Translation Options:")
        while True:
            plaintext = str(input("Enter plaintext: "))
            if plaintext == "#!ERRORCODE!#": exit()
            try:
                temp = Translation_Braille(plaintext, Braille_Proficiency_Level(1))
                translation_proficiency_level = Braille_Proficiency_Level.input_from_console()
                try:
                    return Translation_Braille(plaintext, translation_proficiency_level)
                except:
                    print("Invalid. Please try again.")
            except:
                print("Invalid. Please try again.")
    
    def print(self):
        print(f'''Translation: 
- Plaintext = {self.plaintext}
- Proficiency level = {self.translation_proficiency_level.name}
- Braille = {self.braille_text}
        ''')
    
    '''
    @classmethod
    def from_DataFrame_tuple(cls, dataframe_tuple):
        index, row_tuple = dataframe_tuple
        # plaintext, translation_proficiency_level, braille, search_key = index
        return row_tuple # cls(plaintext, translation_proficiency_level, braille, search_key)
    ''' 
    @classmethod
    def from_Series(cls, series):
        print(series.tolist())
        return cls(series.iloc[0], series.iloc[1], series.iloc[2], series.iloc[3])