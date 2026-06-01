from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# --------------------------------------------
# 회원 가입 요청 모델 정의
# --------------------------------------------
class MemberJoinRequest(BaseModel):
    mid: Annotated[str, Field(min_length=5, max_length=20)] # 필수값
    mname: Annotated[str, Field(min_length=2, max_length=20)] # 필수값
    mpassword: Annotated[str, Field(min_length=5, max_length=20)] # 필수값
    memail: EmailStr # 필수값
    menabled: bool = True # 옵션값
    mrole: Annotated[str, Field(pattern="^(ROLE_USER | ROLE_ADMIN)$")] = "ROLE_USER" # 옵션값
    
# --------------------------------------------
# 회원 가입 응답 모델 정의
# --------------------------------------------
class MemberJoinResponse(BaseModel):
    mid: str
    mname: str
    mpassword: str
    memail: str
    menabled: bool
    mrole: str
    # model_validate()로 해당 모델 객체를 생성할 수 있도록 설정
    # - from_attributes=False (기본값): dict, 다른 Pydantic 모델만 허용
    # - from_attributes=True: ORM, dict, @dataclass, 일반 객체 등 .속성명으로 접근 가능한 모든 객체 허용
    model_config = ConfigDict(from_attributes=True)