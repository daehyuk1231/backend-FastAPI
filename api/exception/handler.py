import logging

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# =================================================
# 404 Not Found 처리기
# =================================================
from fastapi import FastAPI, HTTPException, Request

# 유효성 검사 예외가 발생했을때 처리하는 함수
async def validation_exception_handler(request: Request, e: RequestValidationError):
    logger.info("validation_exception_handler()에서 예외 처리")
    return JSONResponse({
        "error_code": "A0002",
        "message": "잘못된 데이터 전달",
        "detail": e.errors()
    })

# 404 예외가 발생했을때 예외를 처리하는 함수
async def http_404_handler(request: Request, exc: Exception):
    logger.info("http_404_handler()에서 예외 처리")
    return JSONResponse({
        "error_code": "A0001",
        "message": "요청 리소스 없음",
        "detail": f"요청한 {request.url.path}가 존재하지 않습니다."
    })
    
async def http_exception_handler(request: Request, e:HTTPException):
    logger.info("http_exception_handler()에서 예외 처리")
    return JSONResponse({
        "error_code": "A0003",
        "message": "HTTP 에러",
        "detail": e.detail
    })
    
# 사용자 정의 예외 정의
class BusinessException(Exception):
    def __init__(self, 
                 message:str = "",
                 error_code: str = "") -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
        
async def business_exception_handler(request: Request, e: BusinessException):
    logger.info("business_exception_handler() 실행")
    return JSONResponse({
        "error_code": e.error_code,
        "message": "비즈니스 로직 처리 에러",
        "detail": e.message
    })
    
async def general_exception_handler(request: Request, e: Exception):
    return JSONResponse({
        "error_code": "A0005",
        "message": "기타 예외가 발생했음",
        "detail": str(e)
    })
    
# =================================================
# 예외 처리기 일괄 등록 함수
# =================================================
def register_exception_handler(app: FastAPI):
    app.exception_handler(404)(http_404_handler)
    app.exception_handler(RequestValidationError)(validation_exception_handler)
    app.exception_handler(HTTPException)(http_exception_handler)
    app.exception_handler(BusinessException)(business_exception_handler)
    app.exception_handler(Exception)(general_exception_handler)