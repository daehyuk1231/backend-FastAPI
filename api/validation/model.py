import re
from typing import Annotated, Self

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

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
    
    @field_validator("mpassword", "mpassword_confirm")
    @classmethod
    def password_check(cls, v: str) -> str:
        """비밀번호에 영문·숫자·특수문자가 각각 1자 이상 포함되어야 함"""
        if not re.search(r'[A-Za-z]', v):
            raise RequestValidationError("비밀번호에 영문자가 1자 이상 포함되어야 합니다.")
        if not re.search(r'\d', v):
            raise RequestValidationError("비밀번호에 숫자가 1자 이상 포함되어야 합니다.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', v):
            raise RequestValidationError("비밀번호에 특수문자가 1자 이상 포함되어야 합니다.")
        return v
    
    @model_validator(mode="after")
    def password_match(self) -> Self:
        """비밀번호와 비밀번호 확인이 일치해야 함"""
        if self.mpassword != self.mpassword_confirm:
            raise RequestValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return self