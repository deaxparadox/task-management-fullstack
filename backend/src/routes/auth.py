from datetime import datetime, timedelta
import logging
import typing
from uuid import uuid4

from fastapi import (
    APIRouter, 
    status, 
    Depends,
    Request,
    BackgroundTasks
)
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
import pyotp
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound

from src import settings
from src.database import get_db
from src.models.address import Address
from src.models.blacklist import BlackList
from src.models.user import User, UserType
from src.models.validation import Validation
from src.serializer import auth as auth_serializer
from src.serializer import IndexSerializer
from src.utils.mixins import (
    LoginMixin,
    UserCreateMixin
)
from src.utils.otp import OTP
from src.utils import (
    account_activation_link_message,
    account_activation_otp_message,
    decode_string,
    encode_string
)
from src.utils.mail import (
    send_account_activation_mail
)
from src.utils.validation import (
    check_mail_exists,
    check_phone_exists,
    check_username_exists,
    password_validation
)


logger = logging.getLogger(__name__)
router = APIRouter()
cache_backend = FastAPICache()




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
    user_mixin = UserCreateMixin(),
    otp: str | None = None
):
    """
    Register a new user.
    """
    
    # check username existence
    user_exist = await check_username_exists(db, User, user_details.username)
    if user_exist:
        return JSONResponse(dict(message="Username taken"), status_code=status.HTTP_302_FOUND)
    
    # check email existence
    email_exist = await check_mail_exists(db, User, user_details.email)
    if email_exist:
        return JSONResponse(dict(message="Email ID already registered"), status_code=status.HTTP_302_FOUND)
    
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
    
    if otp == "yes":
        
        otp_instance = OTP(db)
        otp_instance.generate()
        user_otp = otp_instance.otp
        user_otp_counter = otp_instance.otp_counter
        current_time = datetime.now()
        
        # encode user name and send in mail
        encoded_data = encode_string(
            username=user_details.username, 
            otp_counter=user_otp_counter,
            current_time=current_time.isoformat()
        )
        mail_message = account_activation_otp_message(request, encoded_data, user_otp)
        new_message + " A OTP has been send to the your email. Please verify the OTP"
        if not await send_account_activation_mail(
            background_tasks,
            user_details.email, 
            mail_message
        ):
            logger.critical("Unable to send OTP email to username: {username}")
            return JSONResponse(
                {"message": "Unable to send OTP email to user for activating the account."}, 
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
    else:
        new_message + "Account activation link has been sent you email. Click on the link to activate the account."
        mail_message = account_activation_link_message(request, new_user)
        if not await send_account_activation_mail(
            background_tasks,
            user_details.email, 
            mail_message
        ):
            #
            logger.critical("Unable to send email to username: {username}")
            return JSONResponse(
                {"message": "Unable to send email to user for activating the account"}, 
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
    return JSONResponse(
        dict(message=new_message),
        status_code=status.HTTP_201_CREATED
    )


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
        return JSONResponse(
            {"message": "Internal Error"}, 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if user.account_activation_id != activation_id:
        # log to server, this should not happen
        logger.error(f"Username {username} and activation ID {activation_id} didn't match")
        return JSONResponse(
            {"message": "Internal server flow error"}, 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    user.account_activation = True
    db.add(user)
    db.commit()
    
    return JSONResponse(
        {"message": "User account activated successfully"}, 
        status_code=status.HTTP_200_OK
    )


@router.post(
    "/otp/{data_string}",
    response_model = IndexSerializer
)
async def activate_user_account_otp(
    data_string, 
    otp_serializer: auth_serializer.OTPSerializer,
    db: Session = Depends(get_db)
):
    """
    Activate user account, based on OTP_EXPIRE_TIME config.
    """
    decoded_string = decode_string(data_string)
    
    # check data string in blacklist.
    blacklisting_check = db.query(BlackList).filter_by(key=data_string).all()
    if len(blacklisting_check) > 0:
        return JSONResponse(
            {"message": "OTP expired"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    username = decoded_string.get("username")
    user_otp_counter = decoded_string.get("otp_counter")
    old_current_time = datetime.fromisoformat(decoded_string.get('current_time'))
    
    new_current_time = datetime.now()
    if new_current_time > (old_current_time + timedelta(minutes=int(settings.OTP_EXPIRE_TIME))):
        return JSONResponse(
            {"message": "OTP expried"},
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    user_instance = db.query(User).filter_by(username=username).one_or_none()
    if not user_instance:
        return JSONResponse(
            {"message": "User not found, invalid otp registration link"}, 
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    hotp = OTP()
    if not hotp.verify(otp_serializer.otp, int(user_otp_counter)):
        return JSONResponse(
            {"message": "Incorrect OTP"}, 
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # activate user account.
    user_instance.account_activation = True 
    # Add the data string to blacklist.
    blacklist = BlackList(key=data_string)
    
    db.add_all([user_instance, blacklist])
    db.commit()
    
    
    return JSONResponse(
        {"message": "User account activated successfully"}, 
        status_code=status.HTTP_202_ACCEPTED
    )




@router.post(
    "/login",
    response_model = auth_serializer.DetailsSerializer
)
async def login_view(
    user_details: auth_serializer.LoginSerializer,
    db: Session = Depends(get_db)
):
    """
    Login with username or email with password.
    """
    if not user_details.username and not user_details.email:
        return JSONResponse(
            {"message": "Required credentials username or email and password"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    login = LoginMixin()
    login.user_model = User
    login.db = db
        
    authentciation = await login.check(username = user_details.username, email = user_details.email, password = user_details.password)
    if authentciation:    
        return JSONResponse(
            {"message": "User login successfully"},
            status_code=status.HTTP_200_OK
        )
    
    return JSONResponse(
        {"message": "Invalid credentials"},
        status_code=status.HTTP_400_BAD_REQUEST
    )
    
    