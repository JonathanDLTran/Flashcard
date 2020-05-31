"""
View.py acts as the View in the Model View Controller paradigm
It formats the information from the controller and model
and prints it out to the user to show
"""
import os
from Constants import *

# https://stackoverflow.com/questions/2084508/clear-terminal-in-python


def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. Useful for managing
    menu screens in terminal applications.
    '''
    os.system('cls||echo -e \\\\033c')


def view():
    print(CLEAR_SCREEN)

    print("".center(NCOLS, "-"))
    print(int(NCOLS/2 - 1) * " " + " " +
          UP_POINT + int(NCOLS/2 - 1) * " ", end="")

    print(LEFT_POINT + int(NCOLS - 2) * " " + RIGHT_POINT, end="")
    print()

    title = "Lambda Calculus"
    centered_title = title.center(NCOLS, "*")
    print(centered_title)
    print()

    diff = "Card: Main"
    ctd_diff = diff.center(NCOLS)
    print(ctd_diff)
    print()

    text = ";osfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsd"
    centered_text = text.center(NCOLS)
    print(centered_text)
    print()

    print(int(NCOLS/2 - 1) * " " + " " +
          DOWN_POINT + int(NCOLS/2 - 1) * " ", end="")
    print("".center(NCOLS, "-"))


if __name__ == "__main__":
    view()
