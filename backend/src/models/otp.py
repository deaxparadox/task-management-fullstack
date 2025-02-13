from sqlalchemy import (
    BigInteger,
    Column
)
from src.database import Base

class Otp(Base):
    __tablename__ = "otp"
    
    counter = Column(BigInteger, primary_key=True, default=0)