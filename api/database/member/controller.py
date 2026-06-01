import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.database.member.entity import MemberEntity
from api.database.member.model import MemberJoinRequest, MemberJoinResponse
from api.database.member.service import MemberServiceDep

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/database/member", tags=["member"])

# ------------------------------------------------
# 회원 가입 엔드포인트 정의
# ------------------------------------------------
@router.post("/join", 
             response_class=JSONResponse, 
             response_model=MemberJoinResponse,
             response_model_exclude={"mpassword"})
async def join(member_join_request:MemberJoinRequest,
               member_service: MemberServiceDep):
    member_entity = MemberEntity(**member_join_request.model_dump())
    member_entity = await member_service.join(member_entity)
    member_join_response = MemberJoinResponse.model_validate(member_entity)
    return member_join_response