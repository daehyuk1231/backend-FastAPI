import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from api.di.service import MemberServiceDep

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/di", tags=["di"])

# 엔드포인트 정의
@router.get("/member-info")
async def member_info(memberService: MemberServiceDep):
    logger.info(id(memberService))
    member = memberService.get_member()
    return member

@router.post("/member-join")
async def member_join(memberService: MemberServiceDep):
    logger.info(id(memberService))
    member = memberService.join()
    return member