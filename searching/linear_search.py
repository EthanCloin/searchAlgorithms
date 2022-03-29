from .search_strategy import SearchStrategy
import time
import curses


class LinearSearch(SearchStrategy):
    """implementation of the most basic search strategy"""

    def __init__(self, screen):
        super().__init__(screen)
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
        """visualize each iteration of linear search algo"""
        PADDING = 5
        DELAY = 1
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
        """idiot testing curses displays"""

        for i in range(3):
            for idx, num in enumerate(nums):
                self.screen.addstr(i, idx * 5, str(num), curses.color_pair(1))
                time.sleep(0.1)
            self.screen.refresh()

        time.sleep(4)
