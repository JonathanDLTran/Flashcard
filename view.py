"""
View.py acts as the View in the Model View Controller paradigm
It formats the information from the controller and model
and prints it out to the user to show
"""
import os
import sys
import curses
from curses import textpad
import asyncio
import traceback
from colorama import init
from termcolor import colored, cprint
import readline
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


def prRed(skk): print("\033[91m{}\033[00m" .format(skk), end="")


def prGreen(skk): print("\033[92m{}\033[00m" .format(skk), end="")


def prYellow(skk): print("\033[93m{}\033[00m" .format(skk), end="")


def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk), end="")


def prPurple(skk): print("\033[95m{}\033[00m" .format(skk), end="")


def prCyan(skk): print("\033[96m{}\033[00m" .format(skk), end="")


def prLightGray(skk): print("\033[97m{}\033[00m" .format(skk), end="")


def prBlack(skk): print("\033[98m{}\033[00m" .format(skk), end="")


def prMagenta(skk): cprint(skk, 'magenta', end="")


def print_red_on_yellow(x): return cprint(x, 'red', 'on_yellow', end="")


def print_black_on_red(x): return cprint(
    x, 'grey', 'on_red', attrs=['bold'], end="")


def print_black_on_cyan(x): return cprint(
    x, 'grey', 'on_cyan', attrs=['bold'], end="")


def print_black_on_green(x): return cprint(
    x, 'grey', 'on_green', attrs=['bold'], end="")


def print_black_on_white(x): return cprint(
    x, 'grey', 'on_white', attrs=['blink', 'reverse'], end="")

# https://stackoverflow.com/questions/27612545/how-to-change-the-location-of-the-pointer-in-python


def move(y, x):
    print("\033[%d;%dH" % (y, x))


def print_help_menu():
    prGreen("This is the help menu.".center(NCOLS))
    prGreen("Type H or Help to enter this menu. \n")
    prGreen("Type E or Exit to exit this menu and return back. \n")

    print("\n")
    prCyan("Review Mode Commands".center(NCOLS))
    prCyan("Type R or Review to enter review mode. \n")
    prCyan("Type F or Front to get to Front of Card \n")
    prCyan("Type R or Rear to get to Rear of Card \n")
    prCyan("Type S or Stats to reveal Card Statistics \n")
    prCyan("Type * or Refresh to refresh Card \n")
    prCyan("Type E or Exit to exit review and return to main. \n")

    print("\n")
    prMagenta("Edit Mode Commands".center(NCOLS))
    prMagenta("Type e or Edit to enter edit mode. \n")
    prMagenta("Type i to start insertion. \n")
    prMagenta("Type d to start deletion. \n")
    prMagenta("Type E or Exit to exit edit mode and return back. \n")

    print("\n")
    prLightPurple("Card Notes Mode Commands".center(NCOLS))
    prLightPurple("Type N or Notes to enter Card Notes \n")
    prLightPurple("Type E or Exit to exit notes mode and return back. \n")

    print("\n")
    prPurple("Global Notes Mode Commands".center(NCOLS))
    prPurple("Type GN or Global-Notes to enter Global Notes \n")
    prPurple("Type E or Exit to exit global notes mode and return back. \n")


def help_view():
    print(CLEAR_SCREEN)
    print("".center(NCOLS, "-"))

    title = " Help Screen "
    centered_title = title.center(NCOLS, "*")
    print_black_on_green(centered_title)
    print()

    print_help_menu()

    print("".center(NCOLS, "-"))

    # modal
    mode = "[HELP MANUAL]"
    print_black_on_green(mode)

    print(" Your Command >$ ", end="")


def test_textpad(stdscr, insert_mode=True):
    ncols, nlines = NCOLS - 4, NROWS - 6
    uly, ulx = 3, 2
    if insert_mode:
        mode = 'insert mode'
    else:
        mode = 'overwrite mode'

    stdscr.addstr(uly-3, ulx, "Use Ctrl-G to end editing (%s)." % mode)
    stdscr.addstr(
        uly-2, ulx, "Be sure to try typing in the lower-right corner.")
    win = curses.newwin(nlines, ncols, uly, ulx)
    win.addstr(uly + 2, ulx, "TO BE REPLACED HERE: LOLOLOL: ")
    textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols)
    stdscr.refresh()

    box = textpad.Textbox(win, insert_mode)

    # textpad.str(uly + 2, ulx, "TO BE REPLACED HERE: LOLOLOL: ")
    contents = box.edit()
    stdscr.addstr(uly+ncols+2, 0, "Text entered in the box\n")
    stdscr.addstr(repr(contents))
    stdscr.addstr('\n')
    stdscr.addstr('Press any key')
    stdscr.getch()

    for i in range(3):
        stdscr.move(uly+ncols+2 + i, 0)
        stdscr.clrtoeol()


def edit_view():
    try:
        # -- Initialize --
        stdscr = curses.initscr()   # initialize curses screen

        curses.noecho()             # turn off auto echoing of keypress on to screen
        curses.cbreak()             # enter break mode where pressing Enter key
        #  after keystroke is not required for it to register
        # enable special Key values such as curses.KEY_LEFT etc
        stdscr.keypad(1)

        # -- Perform an action with Screen --

        test_textpad(stdscr, insert_mode=False)

        while True:
            # stay in this loop till the user presses 'q'
            ch = stdscr.getch()
            if ch == ord('q'):
                break

        # -- End of user code --

    except:
        traceback.print_exc()     # print trace back log of the error

    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


def edit_view2():
    try:
        # -- Initialize --
        stdscr = curses.initscr()   # initialize curses screen

        curses.noecho()             # turn off auto echoing of keypress on to screen
        curses.cbreak()             # enter break mode where pressing Enter key
        #  after keystroke is not required for it to register
        # enable special Key values such as curses.KEY_LEFT etc
        stdscr.keypad(1)

        # -- Perform an action with Screen --
        stdscr.border(0)
        stdscr.addstr(5, 5, 'Hello from Curses!', curses.A_BOLD)
        stdscr.addstr(6, 5, 'Press q to close this screen', curses.A_NORMAL)

        text = (SPLIT_SEQUENCE + "LOL!!!" + SPLIT_SEQUENCE +
                ";osfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdf" +
                "asdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadf" +
                "asdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfaf" +
                "afasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfas" +
                "dfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfs" +
                "fsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfa" +
                "sdfasdfasdfasdfsadfasdfasdfsdfsfsd").center((NCOLS - 8))
        stdscr.addstr(7, 5, text, curses.A_NORMAL)

        test_textpad(stdscr, insert_mode=False)

        while True:
            # stay in this loop till the user presses 'q'
            ch = stdscr.getch()
            if ch == ord('q'):
                break

        # -- End of user code --

    except:
        traceback.print_exc()     # print trace back log of the error

    finally:
        # --- Cleanup on exit ---
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


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
    print_black_on_cyan(centered_title)

    stars = "Star Value : " + STAR + STAR + STAR
    ctd_stars = stars.center(NCOLS)
    print(ctd_stars)

    category = HISTORY + " " + HISTORY + " " + HISTORY
    ctd_category = category.center(NCOLS)
    print(ctd_category)

    diff = "Card: Main"
    ctd_diff = diff.center(NCOLS)
    print(ctd_diff)
    print()

    text = SPLIT_SEQUENCE + "LOL!!!" + SPLIT_SEQUENCE + \
        ";osfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdf" \
        "asdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadf" \
        "asdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfaf" \
        "afasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfas" \
        "dfasdfsadfasdfasdfsdfsfsdosfafafasfgsdgasdfasdfasdfasdfasdfsadfasdfasdfsdfs " \
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
    help_view()
    input()
    edit_view()
    input()
