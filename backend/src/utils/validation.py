from typing import Any, Tuple

from sqlalchemy.orm import Session


async def phone_number_validation(num: Any) -> bool:
    if not isinstance(num, int):
        return False
    count = 0
    while num > 0:
        num //= 10
        count+=1
    if count != 10:
        return False
    return True


async def password_validation(raw_password: str) -> Tuple[bool, str]:
    invalid_message = False, (
        "Password must be atleast 8 characters and atmost 20 characters"
        "and should also include alphanumeric, not special chracter are allowed"
    )
    
    if len(raw_password) < 8 or len(raw_password) > 20:
        return invalid_message
    
    if (
        not any(c.isdigit() for c in raw_password) or 
        not any(c.isupper() for c in raw_password) or
        not any(c.islower() for c in raw_password)  
    ):
        return invalid_message
    
    return True, "Successfull password"


async def check_mail_exists(db_session: Session, user_model, mail_address: str, /) -> bool:
    users = db_session.query(user_model).filter_by(email=mail_address).all()
    if len(users) == 0:
        return False
    return True

async def check_username_exists(db_session: Session, user_model, username: str, /) -> bool:
    users = db_session.query(user_model).filter_by(username=username).all()
    if len(users) == 0:
        return False
    return True

async def check_phone_exists(db_session: Session, user_model, phone: int, /) -> bool:
    users = db_session.query(user_model).filter_by(phone=phone).all()
    if len(users) == 0:
        return False
    return True