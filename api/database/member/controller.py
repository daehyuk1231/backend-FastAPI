import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.database.member.auth import LoginCheckDep, create_token
from api.database.member.entity import MemberEntity
from api.database.member.model import MemberJoinRequest, MemberJoinResponse, MemberLoginRequest, MemberLoginResponse
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
@router.get("/info")
async def info(payload: LoginCheckDep):
    return {"result": "ok"}