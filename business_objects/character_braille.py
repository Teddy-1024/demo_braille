# -*- coding: utf-8 -*-
"""
@author: Edward Middleton-Smith
"""


from typing import Optional, List
from pydantic import BaseModel, field_validator


class Character_Braille(BaseModel):
    plaintext: str
    list_dots_braille: List[bool] 

    def __init__(self, plaintext, list_dots_braille): 
        super().__init__(plaintext=plaintext, list_dots_braille=list_dots_braille)

    @field_validator('list_dots_braille')
    def validate_list_dots_braille(cls, value):
        if (len(value) != 6):
            raise ValueError('List must have rows of 6 colunns')
        if not all(isinstance(dot, bool) for dot in value):
            raise ValueError('List must contain only boolean values')
        return value
    
    @field_validator('plaintext')
    def validate_plaintext(cls, value):
        """
        known_translations = Character_Braille.get_Translation_Brailles()
        if not known_translations['Character_Braille'].apply(lambda x: x.plaintext == value).any():
            raise ValueError('Plaintext not in known translations')
        """
        return value

    def get_blank_character_Braille():
        return Character_Braille("BLANK_SPACE", [0, 0, 0, 0, 0, 0])
    
    def __repr__(self):
        return f'plaintext = {self.plaintext}, list_dots_braille = {self.list_dots_braille}'
