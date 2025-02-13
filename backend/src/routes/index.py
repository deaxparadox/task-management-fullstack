from fastapi import (
    APIRouter, 
    Response, 
    status
)

from src.serializer import IndexSerializer

router = APIRouter()

@router.get(
    "", 
    response_model=IndexSerializer,
    status_code=status.HTTP_200_OK
)
async def index_view():
    return {"message": "Hello Everyone"}
        