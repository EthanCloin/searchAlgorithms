import time
from searching.linear_search import LinearSearch
import curses
from curses import wrapper


def main(stdscr):
    # this main fxn is passed to wrapper to handle initialization
    stdscr.clear()

    # define colors
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)

    test_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    test_target = 7

    search_test = LinearSearch(stdscr)
    # search_test.just_draw_array(test_list)
    search_test.perform_search(test_list, test_target)


wrapper(main)