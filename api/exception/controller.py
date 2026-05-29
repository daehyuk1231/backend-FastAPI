import logging

from fastapi import APIRouter, HTTPException, status

from api.exception.handler import BusinessException

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/exception", tags=["exception"])

# 엔드포인트 정의
@router.get("/http-exception")
async def test_http_exception():
    logger.info("test_http_exception() 실행")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="리소스에 대한 접근 권한이 없음"
    )
    
@router.get("/business-exception")
async def test_business_exception():
    logger.info("test_business_exception() 실행")
    raise BusinessException(
        error_code="A0004",
        message="내부 데이터베이스 연결 실패됨"
    )

@router.get("/unhandled-exception")
async def test_unhandled_exception():
    logger.info("test_unhandled_exception() 실행")
    raise RuntimeError("예상치 못한 런타입 에러가 발생했음")