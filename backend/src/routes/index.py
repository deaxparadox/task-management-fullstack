from fastapi import (
    APIRouter, 
    Response, 
    status
)

from src.schema import IndexSchema

router = APIRouter()

@router.get(
    "", 
    response_model=IndexSchema,
    status_code=status.HTTP_200_OK
)
async def index_view():
    return {"message": "Hello Everyone"}
        