from abc import ABC, abstractmethod
from typing import List, Dict


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict]:
        pass
