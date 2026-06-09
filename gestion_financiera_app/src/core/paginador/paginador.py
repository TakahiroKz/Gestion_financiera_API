from math import ceil
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    item: list[T]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev:bool