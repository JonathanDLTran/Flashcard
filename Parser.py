from Constants import *
# TODO: TARGETS: COMMANDS to implement
#next, last, front, back, forward, rear
# 





def main_parser():
    """

    """
    command = input("Please enter your command, or 'quit' to quit: ")
    if determine_singular(command):
        return singular_commands(command)


def determine_singular(command):
    command = command.strip().lower()
    return SPACE not in command


def singular_commands(command):
    singular_command_dict = {"correctness": correct,
                             "rate": rate,
                             HELP: help_override,
                             QUIT: quit_override}
    if command in singular_command_dict:
        return singular_command_dict[command]()
    print(INVALID_COMMAND)


def help_override():
    print("This is the help module. This project is currently under construction.")
    return HELP


def quit_override():
    print("You are quitting this command. You may enter a new command")
    return QUIT


def correct():
    while(True):
        result = input(
            "Please input 'correct' if you answered correctly. 'incorrect' if you did not, 'skip' to skip, or 'quit' to quit: ")
        cleanedResult = result.strip().lower()
        if cleanedResult == QUIT:
            return quit()
        elif cleanedResult == CORRECT:
            return CORRECT
        elif cleanedResult == INCORRECT:
            return INCORRECT
        elif cleanedResult == SKIP:
            return SKIP
        print(INVALID_COMMAND)


def rate():
    while(True):
        result = input(
            "Please enter a number between 0 and 5 as your rating for the difficulty of this question, or 'quit' to quit: ")
        cleanedResult = result.strip().lower()
        if cleanedResult == QUIT:
            return quit()
        if cleanedResult.isdigit() and int(cleanedResult) in RATE_SCALE_LIST:
            return int(cleanedResult)
        print(INVALID_COMMAND)
