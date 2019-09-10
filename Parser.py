from Flashcard import *
from Constants import *
# TODO: TARGETS: COMMANDS to implement
#next, last, front, back, forward, rear
# 

def parser_driver(deck):
    while(True):
        command = input("Please enter your command: \n").strip().lower()
        if command == "next":
            deck.nextCard()
        elif command == "last":
            deck.lastCard()
        elif command == "forward":
            deck.forwardCard()
        elif command == "rear":
            deck.rearCard()
        elif command == "front" or command == "question":
            deck.frontCard()
        elif command == "back" or command == "answer":
            deck.backCard()
        elif command == "main":
            deck.mainCard()
        elif command == "entire":
            deck.entireCard()
        elif command == "rate":
            result = rate_Card()
            if result == QUIT:
                return
            deck.rateCard(result)
        elif command == "correct":
            result = correct_Card()
            if result == QUIT:
                return
            if result == "correct":
                result = True
            elif result == "incorrect":
                result = False
            deck.correctCard(result)
        elif command == "rating":
            deck.getRate()
        elif command == 'statistics':
            deck.getCorrect()
        elif command == "reset":
            deck.resetCard()
        elif command == "help":
            help_override()
        elif command == "quit":
            return
        else:
            print("@@@@@ NOT A VALID COMMAND @@@@@")
# def parser_driver(deck):
#     while(True):
#         result = main_parser()
#         command = singular_commands(command)
#         if command == QUIT:
#             return
#         deck.command()
        



def main_parser():
    """

    """
    command = input("Please enter your command, or 'quit' to quit: ")
    if determine_singular(command):
        return singular_commands(command)
    return False

def determine_singular(command):
    command = command.strip().lower()
    return SPACE not in command


def singular_commands(command):
    singular_command_dict = {"correctness": correctCard,
                             "rate": rateCard,
                             "next": nextCard,
                             "last": lastCard,
                             "front": frontCard,
                             "back": backCard,
                             "forward": forwardCard,
                             "rear": rearCard,
                             "main": mainCard,
                             HELP: help_override,
                             QUIT: quit_override}
    if command in singular_command_dict:
        return singular_command_dict[command]
    print(INVALID_COMMAND)


def help_override():
    print("This is the help module. This project is currently under construction.")
    return HELP


def quit_override():
    print("You are quitting this command. You may enter a new command")
    return QUIT


def correct_Card():
    while(True):
        result = input(
            "Please input 'correct' if you answered correctly. 'incorrect' if you did not, 'skip' to skip, or 'quit' to quit: ")
        cleanedResult = result.strip().lower()
        if cleanedResult == QUIT:
            return QUIT
        elif cleanedResult == CORRECT:
            return CORRECT
        elif cleanedResult == INCORRECT:
            return INCORRECT
        elif cleanedResult == SKIP:
            return SKIP
        print(INVALID_COMMAND)


def rate_Card():
    while(True):
        result = input(
            "Please enter a number between 0 and 5 as your rating for the difficulty of this question, or 'quit' to quit: ")
        cleanedResult = result.strip().lower()
        if cleanedResult == QUIT:
            return QUIT
        if cleanedResult.isdigit() and int(cleanedResult) in RATE_SCALE_LIST:
            return int(cleanedResult)
        print(INVALID_COMMAND)
