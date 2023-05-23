""" A module for the presentation layer"""

import os
import typing as t
from src.commands import Command

class Option:
    def __init__(
        self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        if isinstance(result, list):
            for line in result:
                print(line)
        else:
            print(result)

    def __str__(self):
        return self.name
    
def print_options(options: t.Dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()

def option_choice_is_valid(choice: str, options: t.Dict[str, Option]) -> bool:
    result = choice in options or choice.upper() in options
    return result

def get_option_choice(options: t.Dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")

        choice = input("Choose an option: ")
    return options[choice.upper()]

def get_user_input(label: str, required: bool = True) -> t.Optional[str]:
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value

def get_new_forecasts()->t.Dict[str, str]: #necessary?
    result = {
        "number_of_container": get_user_input("number_of_container"),
        "port_of_loading": get_user_input("port_of_loading"),
        "port_of_destination": get_user_input("port_of_destination"),
        "date_of_departure_port": get_user_input("date_of_departure_port"),
        "due_date_plant": get_user_input("due_date_plant"),
        }
    return result

def get_forecast_id()-> int:
    result = int(get_user_input("Enter a forecast ID"))  # type: ignore
    return result


def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)