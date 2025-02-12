from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schema import auth as auth_serializer
from src.models.user import User
from src.models.address import Address
from src.models.validation import Validation

router = APIRouter()

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=auth_serializer.DetailsSerializer
)
async def register_user(
    user_details: auth_serializer.RegisterSerializer,
    db: Session = Depends(get_db)
):
    user_data = user_details.model_dump()
    
    users = db.query(User).all()
    print(users)
    
    user_data.update({'id': 1})
    return user_data