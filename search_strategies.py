import time
from abc import ABC, abstractmethod
import curses
from curses import wrapper


class SearchMethod(ABC):

    @abstractmethod
    def perform_search(self, nums, target):
        pass

    @abstractmethod
    def draw_array(self, nums, cur_num, iteration, solution_found=False):
        pass


class LinearSearch(SearchMethod):
    SPACING = 5
    DELAY = 0.5

    def __init__(self, screen):
        self.screen = screen
        self.visited = []

    def perform_search(self, nums: list, target: int):
        """do the searching"""

        for idx, cur_num in enumerate(nums):
            if cur_num is target:
                self.draw_array(nums, cur_num, idx, solution_found=True, solution_idx=idx)
                return idx

            self.visited.append(cur_num)
            self.draw_array(nums, cur_num, idx)

    def draw_array(self, nums, cur_num, row, solution_found=False, solution_idx=-1):
        PADDING = 5
        DELAY = 2
        CYAN = curses.color_pair(1)
        RED = curses.color_pair(2)
        GREEN = curses.color_pair(3)

        # special case of solution reached
        if solution_found:
            for idx, num in enumerate(nums):
                num_str = str(num)

                # stop visualizing search if solution
                if idx == solution_idx:
                    idx *= PADDING
                    self.screen.addstr(row, idx, num_str, GREEN)
                    self.screen.refresh()
                    time.sleep(DELAY * 5)
                    return

                idx *= PADDING
                if num in self.visited:
                    self.screen.addstr(row, idx, num_str, RED)
                else:
                    self.screen.addstr(row, idx, num, CYAN)
                self.screen.refresh()
            return

        # base case of looking
        for idx, num in enumerate(nums):
            idx *= PADDING
            num_str = str(num)
            if num in self.visited:
                self.screen.addstr(row, idx, num_str, RED)
                self.screen.refresh()
            else:
                self.screen.addstr(row, idx, num_str, CYAN)
                self.screen.refresh()
        time.sleep(DELAY)

    def just_draw_array(self, nums):
        # time.sleep(4)

        for i in range(3):
            for idx, num in enumerate(nums):
                self.screen.addstr(i, idx * 5, str(num), curses.color_pair(1))
                time.sleep(0.1)
            self.screen.refresh()

        # for i in range(3):
        #     for idx, num in enumerate(nums):
        #         self.screen.addstr(i, idx * 5, str(num), curses.color_pair(1))
        #         time.sleep(0.1)
        #     self.screen.refresh()

        time.sleep(4)


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
