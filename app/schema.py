from pydantic import BaseModel
from typing import Tuple


class User(BaseModel):
    index: int
    id: str
    robot_model: str = None
    code: str = None
    class Config:
        orm_mode = True