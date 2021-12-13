from pydantic import BaseModel
from typing import Tuple, Enum
import enum


class User(BaseModel):
    index: int
    id: str
    robot_model: str = None
    code: str = None
    class Config:
        orm_mode = True


@enum.unique
class RobotModel(Enum):
    ELEGOOV2 = enum.auto()

class Robot(BaseModel):
    id: str
    model: RobotModel
    current: str
    last: str = ""
