from abc import ABC, abstractmethod


class SearchStrategy(ABC):

    @abstractmethod
    def perform_search(self, nums, target):
        pass

    @abstractmethod
    def draw_array(self, nums, cur_num, iteration, solution_found=False):
        pass
