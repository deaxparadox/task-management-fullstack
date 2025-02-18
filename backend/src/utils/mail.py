from importlib import import_module

from fastapi_mail import (
    FastMail, 
    MessageSchema, 
    MessageType
)

from src import settings


async def send_account_activation_mail(background_tasks, recipients: str, message: str, subject: str, /):
    try:
        msg = MessageSchema(
            subject=subject,
            recipients=[recipients],
            body=message,
            subtype=MessageType.html
        )
        fm = FastMail(settings.mail_config)
        background_tasks.add_task(fm.send_message, msg)
        return True
    
    except Exception as e:
        return False

async def send_password_reset_mail(recipients: str, message: str):
    try:
        msg = MessageSchema(
            subject='Task mansgement: Password reset',
            recipients=[recipients],
            body=message
        )
        fm = FastMail(settings.mail_config)
        fm.send_message(msg)
        return True
    
    except Exception as e:
        return False
    
    
async def send_otp_link_mail(background_task, recipients: str, message: str):
    try:
        msg = MessageSchema(
            subject='User management login',
            recipients=[recipients],
            body=message,
            subtype=MessageType.html
        )
        fm = FastMail(settings.mail_config)
        background_task.add_task(fm.send_message, msg)
        return True
    
    except Exception as e:
        print(f"\n\n{e}\n\n")
        return False
     