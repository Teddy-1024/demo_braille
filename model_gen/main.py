# -*- coding: utf-8 -*-
"""
@author: Edward Middleton-Smith
"""

from translation_braille import Translation_Braille

if __name__ == '__main__':
    print()
    print('Welcome to your Braille Translator')
    print("At any time, answer the following error code to exit (excl. speech marks): '#!ERRORCODE!#'")
    print()
    translation = Translation_Braille.input_from_console()
    print(f'Translation: {translation}')