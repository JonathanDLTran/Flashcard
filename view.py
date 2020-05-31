"""
View.py acts as the View in the Model View Controller paradigm
It formats the information from the controller and model
and prints it out to the user to show
"""
import os
import sys
from colorama import init
from termcolor import colored, cprint
from Constants import *

# https://stackoverflow.com/questions/2084508/clear-terminal-in-python


def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    '''
    os.system('cls||echo -e \\\\033c')

# https://www.geeksforgeeks.org/print-colors-python-terminal/


def prRed(skk): print("\033[91m {}\033[00m" .format(skk), end="")


def prGreen(skk): print("\033[92m {}\033[00m" .format(skk), end="")


def prYellow(skk): print("\033[93m {}\033[00m" .format(skk), end="")


def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk), end="")


def prPurple(skk): print("\033[95m {}\033[00m" .format(skk), end="")


def prCyan(skk): print("\033[96m {}\033[00m" .format(skk), end="")


def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk), end="")


def prBlack(skk): print("\033[98m {}\033[00m" .format(skk), end="")


def print_red_on_yellow(x): return cprint(x, 'red', 'on_yellow', end="")


def print_black_on_cyan(x): return cprint(
    x, 'grey', 'on_cyan', attrs=['bold'], end="")


def print_black_on_white(x): return cprint(
    x, 'grey', 'on_white', attrs=['blink', 'reverse'], end="")


def help_view():
    print(CLEAR_SCREEN)
    print("".center(NCOLS, "-"))

    title = "Help Screen"
    centered_title = title.center(NCOLS, "*")
    print(centered_title)
    print()

    print("".center(NCOLS, "-"))


def rear_view():
    pass


def front_view():
    print(CLEAR_SCREEN)

    print("".center(NCOLS, "-"))
    print(int(NCOLS/2 - 1) * " " + " " +
          UP_POINT + int(NCOLS/2 - 1) * " ", end="")

    print(LEFT_POINT + int(NCOLS - 2) * " " + RIGHT_POINT, end="")

    title = "Lambda Calculus"
    centered_title = title.center(NCOLS, "*")
    print(centered_title)
    print()

    diff = "Card: Main"
    ctd_diff = diff.center(NCOLS)
    print(ctd_diff)
    print()

    text = SPLIT_SEQUENCE + "LOL!!!" + SPLIT_SEQUENCE + \
        ";osfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdf" \
        "asdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadf" \
        "asdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfaf" \
        "afasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfas" \
        "dfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfs "\
        "fsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfa" \
        "sdfasdfasdfasdfsadfasdfasdfsdfsfsd"

    highlighted_text = text.split(SPLIT_SEQUENCE)
    for i in range(len(highlighted_text)):
        if (i == 1):
            print_red_on_yellow(highlighted_text[i])
        else:
            prCyan(highlighted_text[i])
    print()

    print(int(NCOLS/2 - 1) * " " + " " +
          DOWN_POINT + int(NCOLS/2 - 1) * " ", end="")
    print("".center(NCOLS, "-"))

    mode = "[Review Mode]"
    print_black_on_cyan(mode)

    print(" Your Command >$ ", end="")


if __name__ == "__main__":
    front_view()
    input()
    # help_view()
