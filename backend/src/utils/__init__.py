from fastapi import Request
import json
import base64


from .. import settings

def account_activation_link_message(request: Request, user_model):
    if request.url.port:
        link = f"{request.url.scheme}://{":".join([request.url.hostname, str(request.url.port)])}/api/auth/register/{user_model.username}/{user_model.account_activation_id}"
    else:
        link = f"{request.url.scheme}://{request.url.hostname}/api/auth/register/{user_model.username}/{user_model.account_activation_id}"
    message = (
        f"Click on the following link to activate your account: {link}"
    )
    return message

def password_reset_link(request, encoded_string: str):
    return f"{request.scheme}://{":".join([str(x) for x in request.server])}/api/auth/password-reset-unknown/{encoded_string}"

def account_activation_otp_message(request, encoded_string, user_otp, /):
    if request.url.port:
        link = f"{request.url.scheme}://{":".join([request.url.hostname, str(request.url.port)])}/api/auth/otp/{encoded_string}"
    else:   
        link = f"{request.url.scheme}://{request.url.hostname}/api/auth/otp/{encoded_string}"
    message = (
        f"Click on the following link to verify the OTP: {link}\n"
        f"You OTP for activating the account is: {user_otp}"
    )
    return message
        


def encode_string(**kargs) -> str:
    return base64.b64encode(
        json.dumps(kargs).encode(settings.ENCODING)
        ).decode(settings.ENCODING)
    
def decode_string(encoded_string: str) -> str:
    decoded_bytes = base64.b64decode(encoded_string.encode(settings.ENCODING))
    return json.loads(decoded_bytes)