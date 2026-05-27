import logging
import os
import time
from typing import Annotated
from fastapi import APIRouter, Body, Header, Query, UploadFile
from pathlib import Path
from fastapi.params import Form
from api.receivedata.model import BodyJsonRequest, BodyMultipartFormRequest, BodyUrlEncodedRequest

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/receive-data", tags=["receive-data"])

# 엔드포인트 정의
@router.get("/auto-query-string")
async def auto_query_string(mid: str, bno: int = 1):
    logger.info(f"mid: {mid}, bno: {bno}")
    return {"mid": mid, "bno": bno}

@router.get("/auto-path-variable/{mid}/{bno}")
async def auto_path_Variable(mid: str, bno: int = 1):
    logger.info(f"mid: {mid}, bno: {bno}")
    return {"mid": mid, "bno": bno}

@router.post("/auto-body-json")
async def auto_body_json(bodyJsonRequest: BodyJsonRequest):
    logger.info(f"mid: {bodyJsonRequest.mid}, bno: {bodyJsonRequest.bno}")
    return bodyJsonRequest

@router.get("/fun-query")
async def fun_query(
    mid: Annotated[str, Query(alias="member_id")],
    bno: Annotated[int, Query(alias="board_no")] = 1
):
    logger.info(f"mid: {mid}, bno: {bno}")
    return {"mid": mid, "bno": bno}

@router.get("/fun-path/{member_id}/{board_no}")
async def fun_path(
    mid: Annotated[str, Path(alias="member_id")],
    bno: Annotated[int, Path(alias="board_no")]
):
    logger.info(f"mid: {mid}, bno: {bno}")
    return {"mid": mid, "bno": bno}

# 요청 본문: json
@router.post("/fun-body")
async def fun_body(dto: Annotated[BodyJsonRequest, Body]):
    logger.info(f"mid: {dto.mid}, bno: {dto.bno}")
    return dto

# 요청 본문의 x-www-form-urlencoded
@router.post("/fun-form-1")
async def fun_from_1(dto: Annotated[BodyUrlEncodedRequest, Form()]):
    logger.info(f"mid: {dto.mid}, bno: {dto.bno}")
    return dto

# 요청 본문: form-data(multipart)
@router.post("/fun-form-2")
async def fun_from_2(dto : Annotated[BodyMultipartFormRequest, Form()]):
    logger.info(f"btitle: {dto.btitle}")
    if dto.battach and dto.battach.filename:
        # 파일 정보 얻기
        logger.info(f"파일명: {dto.battach.filename}")
        logger.info(f"파일타입: {dto.battach.content_type}")
        
        # 파일 데이터를 서버 파일 시스템에 저장
        contents = await dto.battach.read()
        save_file = f"{time.time_ns()}-{dto.battach.filename}"
        save_dir = Path.home() / "Desktop" / "kosa-course" / "temp"
        os.makedirs(save_dir, exist_ok=True)
        abs_path = os.path.join(save_dir, save_file)
        with open(abs_path, "bw") as file:
            file.write(contents)
        
        return {
        "btitle": dto.btitle,
        "battach" : dto.battach.filename
    }
    else:
        logger.info("파일이 업로드 안됨")
        return {
            "btitle": dto.btitle
        }
        
# @router.post("/fun-form-2")
# async def fun_from_2(
#     btitle: Annotated[str, Form()],
#     battach: Annotated[UploadFile|None, Form()] = None
# ):
#     logger.info(f"btitle: {btitle}")
#     if battach and battach.filename:
#         # 파일 정보 얻기
#         logger.info(f"파일명: {battach.filename}")
#         logger.info(f"파일타입: {battach.content_type}")
        
#         # 파일 데이터를 서버 파일 시스템에 저장
#         contents = await battach.read()
#         save_file = f"{time.time_ns()}-{battach.filename}"
#         save_dir = Path.home() / "Desktop" / "kosa-course" / "temp"
#         os.makedirs(save_dir, exist_ok=True)
#         abs_path = os.path.join(save_dir, save_file)
#         with open(abs_path, "bw") as file:
#             file.write(contents)
        
#         return {
#         "btitle": btitle,
#         "battach" : battach.filename
#     }
#     else:
#         logger.info("파일이 업로드 안됨")
#         return {
#             "btitle": btitle
#         }

@router.get("/fun-header")
async def fun_header(
    user_agent: Annotated[str|None, Header(alias="User-Agent")] = None
):
    logger.info(f"user_agent: {user_agent}")
    return {"user_agent": user_agent}