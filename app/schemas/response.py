from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    success: bool
    message: str = "success"
    data: Optional[T] = None