import collections

from .search_strategy import SearchStrategy
import curses
import time

Bounds = collections.namedtuple('Bounds', ('lower', 'upper'))


class BinarySearch(SearchStrategy):

    def __init__(self, screen):
        super().__init__(screen)
        self.visited = []
        self.exec_log = []

    def perform_search(self, nums, target):
        # init bounds
        lower_bound = 0
        upper_bound = len(nums) - 1
        midpt = (upper_bound + lower_bound) // 2
        iteration = 0

        while True:
            # check if bounds get out of whack aka no solution
            if lower_bound > upper_bound or midpt > upper_bound or midpt < lower_bound:
                return -1

            # check for solution
            if nums[midpt] == target:
                self.draw_array(nums, nums[midpt], iteration, solution_found=True, solution_idx=midpt,
                                bounds=Bounds(lower_bound, upper_bound))
                time.sleep(10)
                return midpt

            if nums[midpt] < target:
                # confine search to the right half
                self.draw_array(nums, nums[midpt], iteration, bounds=Bounds(lower_bound, upper_bound))
                lower_bound = midpt + 1
                midpt = (upper_bound + lower_bound) // 2
            elif nums[midpt] > target:
                # confine search to the left half
                self.draw_array(nums, nums[midpt], iteration, bounds=Bounds(lower_bound, upper_bound))
                upper_bound = midpt - 1
                midpt = (upper_bound + lower_bound) // 2
            iteration += 1

    def draw_array(self, nums, cur_num, iteration, solution_found=False, solution_idx=-1, bounds: Bounds = None):

        PADDING = 4  # used for both column spacing and window offset
        DELAY = 2
        CYAN = curses.color_pair(1)
        RED = curses.color_pair(2)
        GREEN = curses.color_pair(3)
        YELLOW = curses.color_pair(4)
        BLACK = curses.color_pair(5)
        HEADER_MSG = "Performing a Binary Search!\n"

        @staticmethod
        def update_status(status_window, msg):
            """display the supplied message in the status window"""
            status_window.clear()
            status_window.addstr(HEADER_MSG + msg)
            status_window.refresh()

        status_window = curses.newwin(PADDING, 30, 0, 0)
        status_window.clear()
        self.screen.refresh()
        time.sleep(3)
        status_window.refresh()

        for idx, num in enumerate(nums):
            # paint all as yellow first
            str_num = str(num)
            idx_padded = idx * PADDING
            iter_padded = iteration + PADDING
            self.screen.addstr(iter_padded, idx_padded, str_num, YELLOW)
        self.screen.refresh()

        for idx, num in enumerate(nums):
            str_num = str(num)
            idx_padded = idx * PADDING
            iter_padded = iteration + PADDING

            # paint solution green
            if idx == solution_idx:
                self.screen.addstr(iter_padded, idx_padded, str_num, GREEN)
                continue
            # paint bounds cyan
            elif idx == bounds.lower or idx == bounds.upper:
                self.screen.addstr(iter_padded, idx_padded, str_num, CYAN)
                continue
            # paint out of bounds black
            elif idx < bounds.lower:
                self.screen.addstr(iter_padded, idx_padded, str_num, BLACK)
            elif idx > bounds.upper:
                self.screen.addstr(iter_padded, idx_padded, str_num, BLACK)

            self.screen.refresh()
        time.sleep(DELAY)
