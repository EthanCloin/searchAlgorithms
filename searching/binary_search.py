import collections
import sys

from .search_strategy import SearchStrategy
import curses
import time

Bounds = collections.namedtuple('Bounds', ('lower', 'upper'))


class BinarySearch(SearchStrategy):

    H_PADDING = 4  # used for column spacing
    V_PADDING = 4  # used for row spacing
    OFFSET = 15  # used for relative pos from status_window - not used at all actually
    # LONG_DELAY = 5
    # SHORT_DELAY = 2
    STATUS_WIN_CONFIG = (10, 50, 15, 0)

    def __init__(self, screen):
        super().__init__(screen)
        self.visited = []
        self.exec_log = []
        self.status_window = curses.newwin(*self.STATUS_WIN_CONFIG)

        self.EXIT_KEY = "q"
        self.CONTINUE_KEY = "n"
        self.CYAN = curses.color_pair(1)
        self.RED = curses.color_pair(2)
        self.GREEN = curses.color_pair(3)
        self. YELLOW = curses.color_pair(4)
        self.BLACK = curses.color_pair(5)

    def perform_search(self, nums, target):
        # init bounds
        lower_bound = 0
        upper_bound = len(nums) - 1
        midpt = (upper_bound + lower_bound) // 2
        iteration = 0

        while True:
            # check if bounds get out of whack aka no solution
            if lower_bound > upper_bound or midpt > upper_bound or midpt < lower_bound:
                self.update_status(f"Target does not exist!", self.RED)
                return -1

            self.update_status(f"Comparing midpoint:{nums[midpt]} to target:{target}", self.YELLOW)
            # check for solution
            if nums[midpt] == target:
                self.draw_array(nums, nums[midpt], iteration, solution_found=True, solution_idx=midpt,
                                bounds=Bounds(lower_bound, upper_bound))
                self.update_status(f"Target found at index {midpt}!", self.GREEN)
                time.sleep(10)
                return midpt

            if nums[midpt] < target:

                # confine search to the right half
                self.draw_array(nums, nums[midpt], iteration, bounds=Bounds(lower_bound, upper_bound))
                lower_bound = midpt + 1
                midpt = (upper_bound + lower_bound) // 2
                self.update_status(f"{nums[midpt]} is less than {target}...updating search range!", self.CYAN)
                self.update_status(f"\nUpdated Range Indices: ({lower_bound}, {upper_bound})", self.CYAN)
            elif nums[midpt] > target:
                # confine search to the left half
                self.draw_array(nums, nums[midpt], iteration, bounds=Bounds(lower_bound, upper_bound))
                upper_bound = midpt - 1
                midpt = (upper_bound + lower_bound) // 2
                self.update_status(f"{nums[midpt]} is greater than {target}...updating search range!", self.CYAN)
                self.update_status(f"\nUpdated Range Indices: ({lower_bound}, {upper_bound})", self.CYAN)
            iteration += 1

    def draw_array(self, nums, cur_num, iteration, solution_found=False, solution_idx=-1, bounds: Bounds = None):

        # initially draw all numbers yellow
        for idx, num in enumerate(nums):
            # paint all as yellow first
            str_num = str(num)
            idx_padded = idx * self.H_PADDING
            iter_padded = iteration + self.V_PADDING
            self.screen.addstr(iter_padded, idx_padded, str_num, self.YELLOW)
        self.screen.refresh()

        # color bounds cyan, solution green, out of bounds black
        for idx, num in enumerate(nums):
            str_num = str(num)
            idx_padded = idx * self.H_PADDING
            iter_padded = iteration + self.V_PADDING

            # paint solution green
            if idx == solution_idx:
                self.screen.addstr(iter_padded, idx_padded, str_num, self.GREEN)
                continue
            # paint bounds cyan
            elif idx == bounds.lower or idx == bounds.upper:
                self.screen.addstr(iter_padded, idx_padded, str_num, self.CYAN)
                continue
            # paint out of bounds black
            elif idx < bounds.lower:
                self.screen.addstr(iter_padded, idx_padded, str_num, self.BLACK)
            elif idx > bounds.upper:
                self.screen.addstr(iter_padded, idx_padded, str_num, self.BLACK)

            self.screen.refresh()

    def update_status(self, msg, color):
        """display the supplied message in the status window"""

        HEADER_MSG = f"Performing a Binary Search!\n\tPress '{self.CONTINUE_KEY}' to proceed or '{self.EXIT_KEY}' to quit.\n"
        HEADER_LINES = HEADER_MSG.count('\n')
        self.screen.refresh()
        self.status_window.clear()
        self.status_window.addstr(0, 0, HEADER_MSG, self.CYAN)

        self.status_window.addstr(HEADER_LINES + 1, 4, msg, color)
        self.status_window.refresh()
        self.exec_log.append(msg)
        self.screen.refresh()

        while True:
            try:
                user_input = self.screen.getkey()
                # print(user_input)
                if user_input is self.EXIT_KEY:
                    sys.exit(0)
                if user_input is self.CONTINUE_KEY:
                    break

            except (TypeError, Exception) as err:
                print(f'caught {err}')

