import json
import base64


from .. import settings

def account_activation_link(request, user_model):
    return f"{request.scheme}://{":".join([str(x) for x in request.server])}/api/auth/register/{user_model.id}/{user_model.account_activation_id}"

def password_reset_link(request, encoded_string: str):
    return f"{request.scheme}://{":".join([str(x) for x in request.server])}/api/auth/password-reset-unknown/{encoded_string}"

def account_activation_otp(request, encoded_string):
    return f"{request.scheme}://{":".join([str(x) for x in request.server])}/api/auth/otp/{encoded_string}"
        


def encode_string(**kargs) -> str:
    return base64.b64encode(
        json.dumps(kargs).encode(settings.ENCODING)
        ).decode(settings.ENCODING)
    
def decode_string(encoded_string: str) -> str:
    decoded_bytes = base64.b64decode(encoded_string.encode(settings.ENCODING))
    return json.loads(decoded_bytes)