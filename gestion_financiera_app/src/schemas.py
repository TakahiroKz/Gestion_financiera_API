from pydantic import BaseModel

class GenResponse(BaseModel):
    success: bool
    message: str