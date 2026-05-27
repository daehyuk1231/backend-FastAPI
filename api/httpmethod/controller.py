# 로거 생성
import logging
logger = logging.getLogger(__name__)

# 라우터 생성
from fastapi import APIRouter
router = APIRouter(prefix="/http-method", tags=["http-method"])

# 회원가입 엔드포인트 정의
@router.post("/join")
async def join():
    logger.info("회원 가입 처리 로직 실행")
    return {"message": "회원 가입 성공"}

# 로그인 엔드포인트 정의
@router.post("/login")
async def login():
    logger.info("로그인 처리 로직 실행")
    return {
        "mid": "user",
        "access_token": "xxxxxxx.yyyyyyy.zzzzzzz"
    }
    
# 회원 정보 조회 엔드포인트 정의
@router.get("/info")
async def info():
    logger.info("회원 정보 조회 처리 로직 실행")
    return {
        "mid": "user",
        "mname": "홍길동",
        "memail": "hong@mycompany.com"
    }
    
# 회원 수정 엔드포인트 정의
@router.put("/modify")
async def modify():
    logger.info("회원 수정 처리 로직 실행")
    return {
        "message": "회원 수정 성공"
    }
    
# 회원 수정 엔드포인트 정의
@router.delete("/remove")
async def remove():
    logger.info("회원 삭제 처리 로직 실행")
    return {
        "message": "회원 삭제 성공"
    }