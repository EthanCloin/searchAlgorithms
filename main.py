import time
from searching.linear_search import LinearSearch
from searching.binary_search import BinarySearch
import curses
from curses import wrapper


def main(stdscr):
    # this main fxn is passed to wrapper to handle initialization
    stdscr.clear()

    # define colors
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_WHITE, -1)

    # build description window
    # desc_win = curses.newwin(5, 30, 0, 0)
    test_list = [x for x in range(11)]
    test_target = 4
    #
    # search_test = LinearSearch(stdscr)
    # search_test.perform_search(test_list, test_target)

    bs_test = BinarySearch(stdscr)
    # bs_test.update_status("TEST MSG", curses.color_pair(1))
    # time.sleep(10)
    bs_test.perform_search(test_list, test_target)


wrapper(main)