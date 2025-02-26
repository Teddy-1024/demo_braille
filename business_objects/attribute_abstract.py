
"""
@author: Edward Middleton-Smith
Precision And Research Technology Systems Limited
"""

from abc import ABC, abstractmethod
from prettytable import PrettyTable


class Attribute_Abstract(ABC):
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
        print("Please select product configuration from below: ")
        print(table_output)
        while True:
            option = str(input("Product configuration (by index): "))
            print(option + " selected")
            if option == "#!ERRORCODE!#": exit()
            for index_option in range(count_options):
                if option == str(index_option + 1):
                    return options[index_option]
    
    def input_many_from_console(cls):
        selected = []
        print(f'Inputting many {cls.__name__} objects')
        print()
        while True:
            try:
                count_inputs = int(input(f'Quantity of {cls.__name__} objects to enter: '))
            except: continue
            for index_input in range(count_inputs):
                print(f'Inputting {cls.__name__} object {index_input + 1}')
                selected_new = cls.input_from_console(cls)
                selected.append(selected_new)
            break
        return selected
    