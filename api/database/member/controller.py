import logging
from typing import Annotated
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from api.database.member.auth import AdminCheckDep, LoginCheckDep, create_token
from api.database.member.entity import MemberEntity
from api.database.member.model import MemberJoinRequest, MemberJoinResponse, MemberLoginRequest, MemberLoginResponse, MemberModifyRequest, MemberResponse
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

# ------------------------------------------------
# 회원 로그인 엔드포인트 정의
# ------------------------------------------------
@router.post("/login", 
             response_class=JSONResponse, 
             response_model=MemberLoginResponse)
async def login(
    member_login_request: MemberLoginRequest,
    member_service: MemberServiceDep
):
    member_entity = await member_service.login(
        member_login_request.mid, 
        member_login_request.mpassword
    )
    
    mid = member_entity.mid
    mrole = member_entity.mrole
    accessToken = create_token(mid, mrole)
    
    member_login_response = MemberLoginResponse(
        mid=mid,
        accessToken=accessToken
    )
    return member_login_response

# ------------------------------------------------
# 회원 정보 조회 엔드포인트 정의
# ------------------------------------------------
@router.get("/info", 
            response_class=JSONResponse,
            response_model=MemberResponse,
            response_model_exclude={"mpassword"})
async def info(payload: LoginCheckDep, 
               member_service: MemberServiceDep) -> MemberResponse:
    
    mid = payload["sub"]
    member_entity = await member_service.read(mid)
    member_response = MemberResponse.model_validate(member_entity)
    
    return member_response

# ------------------------------------------------
# 회원 수정 엔드포인트 정의
# ------------------------------------------------
@router.put("/modify")
async def modify(
    member_modify_request: MemberModifyRequest,
    payload: LoginCheckDep,
    member_service: MemberServiceDep
):
    member_entity = MemberEntity(**member_modify_request.model_dump())
    member_entity.mid = payload["sub"]
    
    member_entity = await member_service.modify(member_entity)
    member_response = MemberResponse.model_validate(member_entity)
    return member_response

# ------------------------------------------------
# 회원 삭제 엔드포인트 정의
# ------------------------------------------------
@router.delete("/remove/{mid}",
               response_class=JSONResponse)
async def remove(
    mid: str,
    payload: AdminCheckDep,
    member_service: MemberServiceDep
):
    await member_service.remove(mid)
    return {"result": "success"}