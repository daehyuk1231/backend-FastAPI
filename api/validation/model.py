from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

# =======================================
# 회원 가입 요청 모델
# =======================================
class MemberJoinRequest(BaseModel):
    mid: Annotated[str, Field(min_length=4, max_length=20, pattern=r"^[A-Za-z0-9]+$")]
    mname: Annotated[str, Field(min_length=2, max_length=10)]
    mpassword: Annotated[str, Field(min_length=8, max_length=20)]
    mpassword_confirm: Annotated[str, Field(min_length=8, max_length=20)]
    memail: Annotated[EmailStr, Field()]
    mphone: Annotated[str | None, Field(pattern=r"^010\d{3,4}\d{4}$")] = None
    mage: Annotated[int | None, Field(ge=0, le=150, default=None)]