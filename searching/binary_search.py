import collections
import sys
from .search_strategy import SearchStrategy
import curses

Bounds = collections.namedtuple('Bounds', ('lower', 'upper'))


class BinarySearch(SearchStrategy):
    """contains methods to visualize a binary search through an array of ints"""

    H_PADDING = 4  # used for column spacing
    V_PADDING = 4  # used for row spacing
    OFFSET = 15  # used for relative pos from status_window - not used at all actually
    STATUS_WIN_CONFIG = (10, 50, 15, 0)

    def __init__(self, screen):
        super().__init__(screen)
        self.visited = []
        self.exec_log = []
        self.status_window = curses.newwin(*self.STATUS_WIN_CONFIG)
        self.target = -1

        self.EXIT_KEY = "q"
        self.CONTINUE_KEY = "n"
        self.CYAN = curses.color_pair(1)
        self.RED = curses.color_pair(2)
        self.GREEN = curses.color_pair(3)
        self. YELLOW = curses.color_pair(4)
        self.BLACK = curses.color_pair(5)

    def perform_search(self, nums, target):
        """logic of the binary search with some update_status calls"""
        # init bounds
        lower_bound = 0
        upper_bound = len(nums) - 1
        midpt = (upper_bound + lower_bound) // 2
        nums = sorted(nums)
        iteration = 1

        # store target
        self.target = target

        # intro
        self.draw_array(nums, -1, 0)
        self.update_status("beginning the search!", self.CYAN)

        while True:
            # check if bounds get out of whack aka no solution
            if lower_bound > upper_bound or midpt > upper_bound or midpt < lower_bound:
                self.update_status(f"Target does not exist!", self.RED)
                return -1

            # check for solution
            if nums[midpt] == target:
                self.draw_array(nums, nums[midpt], iteration, solution_found=True, solution_idx=midpt,
                                bounds=Bounds(lower_bound, upper_bound))
                return midpt

            if nums[midpt] < target:

                # confine search to the right half
                self.draw_array(nums, nums[midpt], iteration, bounds=Bounds(lower_bound, upper_bound))
                self.update_status(f"{nums[midpt]} is less than {target}...updating search range!", self.CYAN)
                lower_bound = midpt + 1
                midpt = (upper_bound + lower_bound) // 2
            elif nums[midpt] > target:
                # confine search to the left half
                self.draw_array(nums, nums[midpt], iteration, bounds=Bounds(lower_bound, upper_bound))
                self.update_status(f"{nums[midpt]} is greater than {target}...updating search range!", self.CYAN)
                upper_bound = midpt - 1
                midpt = (upper_bound + lower_bound) // 2
            iteration += 1

    def draw_array(self, nums, cur_num, iteration, solution_found=False, solution_idx=-1, bounds: Bounds = None):
        """display the list, calling update_status periodically to allow user control over timing"""

        def pad_idx(index: int) -> int:
            """helper to space numbers properly in display row"""
            return index * self.H_PADDING

        def pad_iter(index: int) -> int:
            """helper to offset rows properly"""
            return index + self.V_PADDING

        # initially draw all numbers yellow
        for idx, num in enumerate(nums):
            self.screen.addstr(pad_iter(iteration), pad_idx(idx), str(num), self.YELLOW)
        self.screen.refresh()

        # special behavior for first call
        if iteration == 0:
            return

        # color bounds cyan, solution green, out of bounds black, midpoint red
        painted = []

        # paint bounds
        self.screen.addstr(pad_iter(iteration), pad_idx(bounds.lower), str(nums[bounds.lower]), self.CYAN)
        self.screen.addstr(pad_iter(iteration), pad_idx(bounds.upper), str(nums[bounds.upper]), self.CYAN)
        painted.append(nums[bounds.lower])
        painted.append(nums[bounds.upper])

        self.update_status(f"\nCurrent Range Indices: ({bounds.lower}, {bounds.upper})", self.CYAN)

        # paint midpoint
        self.screen.addstr(pad_iter(iteration), pad_idx(nums.index(cur_num)), str(cur_num), self.RED)
        painted.append(cur_num)
        self.visited.append(cur_num)
        self.update_status(f"Checking {cur_num} against target: {self.target}", self.YELLOW)

        for idx, num in enumerate(nums):

            # paint solution green
            if idx == solution_idx:
                self.screen.addstr(pad_iter(iteration), pad_idx(idx), str(num), self.GREEN)
                self.update_status(f"Target found at index {solution_idx}!", self.GREEN)
                continue

            # paint visited red
            if num in self.visited:
                self.screen.addstr(pad_iter(iteration), pad_idx(idx), str(num), self.RED)
            # paint out of bounds black
            if idx < bounds.lower and num not in painted:
                self.screen.addstr(pad_iter(iteration), pad_idx(idx), str(num), self.BLACK)
            if idx > bounds.upper and num not in painted:
                self.screen.addstr(pad_iter(iteration), pad_idx(idx), str(num), self.BLACK)

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

