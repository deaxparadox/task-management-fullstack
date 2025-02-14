from sqlalchemy import ( 
    Integer,
    Column,
    String
)
from src.database import Base


class BlackList(Base):
    __tablename__ = "blacklist"
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(2000))