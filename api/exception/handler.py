import logging

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# =================================================
# 404 Not Found 처리기
# =================================================
from fastapi import FastAPI, Request

# 유효성 검사 예외가 발생했을때 처리하는 함수
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.info("validation_exception_handler()에서 예외 처리")
    return JSONResponse({
        "error_code": "A0002",
        "message": "잘못된 데이터 전달",
        "detail": exc.errors()
    })

# 404 예외가 발생했을때 예외를 처리하는 함수
async def http_404_handler(request: Request, exc: Exception):
    logger.info("http_404_handler()에서 예외 처리")
    return JSONResponse({
        "error_code": "A0001",
        "message": "요청 리소스 없음",
        "detail": f"요청한 {request.url.path}가 존재하지 않습니다."
    })
    
# =================================================
# 예외 처리기 일괄 등록 함수
# =================================================
def register_exception_handler(app: FastAPI):
    app.exception_handler(404)(http_404_handler)
    app.exception_handler(RequestValidationError)(validation_exception_handler)