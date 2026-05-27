from fastapi import UploadFile
from pydantic import BaseModel


class BodyJsonRequest(BaseModel):
    mid: str        # 필수값
    bno: int = 1    # 옵션값
    
class BodyUrlEncodedRequest(BaseModel):
    mid: str        # 필수값
    bno: int = 1    # 옵션값
    
class BodyMultipartFormRequest(BaseModel):
    btitle: str                         # 필수값
    battach: UploadFile | None = None   # 옵션값