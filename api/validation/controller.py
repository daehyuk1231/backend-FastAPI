import logging
from typing import Annotated

from fastapi import APIRouter, Body

from api.validation.model import MemberJoinRequest

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/validation", tags=["validation"])

# 엔드포인트 정의
@router.post("/member/join")
async def join(member: Annotated[MemberJoinRequest, Body()]):
    logger.info(member)
    return {"message": "회원가입 성공"}