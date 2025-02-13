import typing
import logging
from uuid import uuid4

from fastapi import (
    APIRouter, 
    status, 
    Depends,
    Request,
    BackgroundTasks
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound

from src.utils import (
    account_activation_link,
    account_activation_otp
)
from src.database import get_db
from src.models.address import Address
from src.models.user import User, UserType
from src.models.validation import Validation
from src.serializer import auth as auth_serializer
from src.serializer import IndexSerializer
from src.utils.mail import (
    send_account_activation_mail
)
from src.utils.validation import (
    password_validation,
    check_mail_exists,
    check_phone_exists,
    check_username_exists
)


logger = logging.getLogger(__name__)
router = APIRouter()


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
            password=User.make_passsword(user_detail.password)
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



@router.post(
    "/register",
    status_code = status.HTTP_201_CREATED,
    response_model = typing.Union[IndexSerializer, auth_serializer.DetailsSerializer]
)
async def register_user(
    user_details: auth_serializer.RegisterSerializer,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_mixin = UserCreateMixin()
):
    """
    Register a new user.
    """
    
    logger.critical("Registering new user.")
    
    # check username existence
    user_exist = await check_username_exists(db, User, user_details.username)
    if user_exist:
        return JSONResponse(dict(message="Username taken"), status_code=status.HTTP_302_FOUND)
    
    # password validation
    pass_status, pass_mes = await password_validation(user_details.password)
    if not pass_status:
        return JSONResponse(
            dict(message=pass_mes), status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # create new user
    new_status, new_message, new_user = await user_mixin.create_user(db, user_details)
    if not new_status:
        return JSONResponse({"message": new_message}, status_code=status.HTTP_400_BAD_REQUEST) 
    
    if not await send_account_activation_mail(
        background_tasks,
        user_details.email, 
        account_activation_link(request, new_user)
    ):
        #
        logger.critical("Unable to send email to username: {username}")
        return JSONResponse({"message": "Unable to send email to user"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    return JSONResponse(dict(message=new_message))


@router.get(
    "/register/{username}/{activation_id}",
    response_model = IndexSerializer
)
async def activate_user_account(username: str, activation_id: str, db: Session = Depends(get_db), user_model = User):
    """
    Activate the user account.
    """
    
    try:
        user: User = db.query(user_model).filter_by(username=username).one_or_none()
    except MultipleResultsFound as e:
        # log the error to the file.
        # this should not happen and return internal error.
        logger.error(f"Mulitple user with same name: {username}")
        return JSONResponse({"message": "Internal Error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if user.account_activation_id != activation_id:
        # log to server, this should not happen
        logger.error(f"Username {username} and activation ID {activation_id} didn't match")
        return JSONResponse({"message": "Internal server flow error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    user.account_activation = True
    db.add(user)
    db.commit()
    
    return JSONResponse({"message": "User account activated successfully"}, status_code=status.HTTP_200_OK)

