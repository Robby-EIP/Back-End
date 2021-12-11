from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import Tuple

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    index = Column(Integer, primary_key=True, index=True)
    id = Column(String)
    robot_model = Column(String)
    code = Column(String)