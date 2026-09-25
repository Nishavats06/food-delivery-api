from pydantic import BaseModel

class GoogleLoginRequest(BaseModel):
    id_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
            }
        }