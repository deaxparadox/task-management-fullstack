from sqlalchemy import (
    Boolean, 
    BigInteger,
    Column, 
    Enum,   
    Integer, 
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from src.database import Base


from src.models.task import Task
from src.utils.security.passwd import generate_hashed_password, check_password
from src.utils.user import UserType


class User(Base):
    __tablename__ = "user"
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(1000))
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    role = Column(Enum(UserType), default=UserType.Employee)
    email = Column(String(120), nullable=True)
    phone = Column(BigInteger, nullable=True)
    
    account_activation = Column(Boolean, default=False, nullable=True)
    account_activation_id = Column(String(36), nullable=True)
    
    # self relation
    
    address = relationship(
        "Address", 
        uselist=False,
        cascade="save-update",
        passive_deletes=True,
        back_populates="user"
    )
    validation = relationship(
        "Validation", 
        uselist=False,
        cascade="save-update",
        passive_deletes=True,
        back_populates="user"
    )
    task_created_by = relationship(
        "Task",
        foreign_keys="Task.created_by_id", 
        uselist=False,
        cascade="save-update",
        passive_deletes=True,
        back_populates="created_by"
    )
    task_assigned_by = relationship(
        "Task",
        foreign_keys="Task.assigned_by_id", 
        uselist=False,
        cascade="save-update",
        passive_deletes=True,
        back_populates="assigned_by"
    )
    task_received = relationship(
        "Task",
        foreign_keys="Task.assigned_to_id", 
        uselist=False,
        cascade="save-update",
        passive_deletes=True,
        back_populates="assigned_to"
    )
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    def set_password(self, raw_passwrod: str) -> None:
        self.password = generate_hashed_password(raw_passwrod)
        
    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)
    
    @staticmethod
    def make_password(raw_password: str) -> str:
        return generate_hashed_password(raw_password)
    
    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in ['password', 'active', 'account_activation', 'account_activation_id']:
            del data[key]
        data['role'] = self.role.value
        return data