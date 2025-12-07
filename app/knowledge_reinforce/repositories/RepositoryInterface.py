from typing import TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar('T', bound='BaseModel')

class RepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def create(self, obj: T) -> T:
        pass

    @abstractmethod
    def update(self, obj: T) -> T | None:
        pass

    @abstractmethod
    def delete(self, obj: T) -> bool:
        pass
