import typing
from uuid import uuid4

from sqlalchemy.orm import Session

from src.models.user import User
from src.serializer import auth as auth_serializer
from src.utils.user import UserType


class UserCreateMixin:
    
    async def create_user(
        self,
        db: Session, 
        user_detail: auth_serializer.RegisterSerializer, 
        /
    ) -> typing.Tuple[bool, str]:
        user = User(
            username=user_detail.username,
            email=user_detail.email,
            password=User.make_password(user_detail.password)
        )
        
        # get user role
        user_role = self.get_user_role(user_detail.role)
        if not user_role:
            return False, "Invalid role selected", None
        
        user.role = user_role
        user.account_activation_id = uuid4()
        db.add(user)
        db.commit()
        db.refresh(user)
        return True, "User created successfully", user

    def get_user_role(self, value, /):
        """
        Return appropriate User roles
        """
        if UserType.Employee.value == value:
            return UserType.Employee
        if UserType.TeamLead.value == value:
            return UserType.TeamLead
        if UserType.Manager.value == value:
            return UserType.Manager
        return 0   

class LoginMixin:
    user_model = None
    db: Session = None
    
    async def get_user(self, *, username: str | None = None, email: str | None = None):
        """
        This function returns the user via username or email
        """
        if username:
            return self.db.query(self.user_model).filter_by(username=username).one_or_none()
        if email:
            return self.db.query(self.user_model).filter_by(email=email).one_or_none()
        return
    
    async def check(self, username: str | None = None, email: str | None = None, password: str | None = None) -> None:
        """
        This function check (username or password) or (email of password), and 
        returns a boolean value
        """
        user = await self.get_user(email=email, username=username)
        if not user:
            return False
        return user.check_password(password)


class UserVerifyMixin:
    checked_user = None
    
    async def check_user_exists(self, username: str, /) -> bool:
        self.checked_user = self.db.query(self.user_model).where(self.user_model.username==username).all()
        if len(self.checked_user) > 0:
            return True
        return False
    
    
    async def check_email_exists(self, email: str, /) -> bool:
        self.checked_user = self.db.query(self.user_model).where(self.user_model.email==email).all()
        print(self.checked_user)
        if len(self.checked_user) > 0:
            return True
        return False
    
    async def check_user_by_id(self, user_id: int, /) -> bool:
        self.checked_user = self.db.query(self.user_model).where(self.user_model.id==user_id).one_or_none()
        if self.checked_user and self.checked_user.active:
            return True
        return False
    

class OTPLoginMixin(LoginMixin, UserVerifyMixin):
    async def login_verify(self, email: str):
        return await self.check_email_exists(email)
    
    async def get_user(self):
        return self.checked_user[0]