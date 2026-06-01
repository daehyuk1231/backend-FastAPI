from datetime import datetime, timedelta, timezone
import logging
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt

# 로거 생성
logger = logging.getLogger(__name__)

# ---------------------------------------------
# JWT 설정 값
# ---------------------------------------------
_SECRET_KEY = "com.mycompany.backendapi.secret.key"
_JWT_DURATION_MS = 24 * 60 * 60 * 1000 # 24h
_ALGORITHM = "HS256"

# ---------------------------------------------
# JWT 토큰 생성
# ---------------------------------------------
def create_token(mid: str, mrole: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        # 로그인한 회원 아이디
        "sub": mid,
        # 회원의 권한(역할)
        "mrole": mrole,
        # 토큰 발급 시간
        "iat": int(now.timestamp()),
        # 토큰 만료 시간
        "exp": int((now + timedelta(milliseconds=_JWT_DURATION_MS)).timestamp())
    }
    jwtStr = jwt.encode(payload, _SECRET_KEY, algorithm=_ALGORITHM)
    return jwtStr

# ---------------------------------------------
# JWT 토큰 추출기 얻기
# ---------------------------------------------
# OAuth2PasswordBearer: OAuth2 스펙에 따른 Bearer 토큰 인증 방식 구현 클래스
# - tokenUrl: 토큰 발급 URL (로그인 API 엔드포인트) 지정
#   문서용 메타데이터(Swagger Authorize 버튼에서 토큰 받는 경우 안내)일 뿐, 
#   토큰을 "그 URL에서 가져온다"는 뜻이 아님
# - auto_error: 토큰이 없을 경우 에러 발생 여부
#   True(기본값) - 토큰 없으면, 자체 401 응답 처리
#   False - 토큰이 없으면 None 반환 (verify_token 함수에서 직접 처리) 
_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/database/member/login",
    auto_error=False
)

# ---------------------------------------------
# JWT에서 페이로드 추출 함수 정의
# ---------------------------------------------
def get_payload(token: str) -> dict:
    try:
        payload = jwt.decode(token, _SECRET_KEY, algorithm=_ALGORITHM)
        if "sub" not in payload:
            raise jwt.MissingRequiredClaimError("토큰안에 회원 아이디가 없음")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="잘못된 토큰이거나 만료된 토큰")
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail=str(e))
        
# ---------------------------------------------
# 의존성 주입을 위한 함수 정의
# ---------------------------------------------
async def verify_access_token(
    request: Request,
    # 요청 HTTP의 헤더에서 Authorization의 값으로 읽을 경우
    access_token: Annotated[str | None, Depends(_oauth2_scheme)] = None
    ) -> dict:
    if not access_token:
        # <img src="/..../accessToken=xxxx"/> 이렇게 요청되었을 경우
        access_token = request.query_params.get("accessToken")
    if not access_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="토큰이 없음")
    payload = get_payload(access_token)
    return payload