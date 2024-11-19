from abc import ABC, abstractmethod


class GetApiHH(ABC):

    @abstractmethod
    def _fetch_data(self):
        pass
