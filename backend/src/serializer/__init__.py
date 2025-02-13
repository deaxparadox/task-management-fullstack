from pydantic import BaseModel

class IndexSerializer(BaseModel):
    message: str