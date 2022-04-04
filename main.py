import time
from searching.linear_search import LinearSearch
from searching.binary_search import BinarySearch
import curses
from curses import wrapper


def main(stdscr):
    """this main function is wrapped by curses to initialize terminal display"""
    # define colors
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_WHITE, -1)

    # define search params
    test_list = [x for x in range(30) if x % 3 == 0]
    test_target = 11

    # search_test = LinearSearch(stdscr)
    # search_test.perform_search(test_list, test_target)

    bs_test = BinarySearch(stdscr)
    bs_test.perform_search(test_list, test_target)


wrapper(main)