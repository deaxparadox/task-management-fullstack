from pydantic import BaseModel, EmailStr

class RegisterSerializer(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: int
    
class AddressSerializer(BaseModel):
    id: int
    line1: str
    line2: str
    city: str
    state: str
    country: str
    pincode: str
    
class DetailsSerializer(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    role: int
    phone: int | None = None
    address: AddressSerializer | None = None
    
class OTPSerializer(BaseModel):
    otp: str
    
class LoginSerializer(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str