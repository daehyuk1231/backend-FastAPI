from datetime import datetime
import logging
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Response, status
from fastapi.responses import JSONResponse

from api.database.board.entity import BoardEntity
from api.database.board.model import BoardListItemResponse, BoardListResponse, BoardResponse, BoardUpdateRequest, BoardWriteRequest, Pager
from api.database.board.service import BoardServiceDep
from api.database.member.auth import LoginCheckDep
from api.exception.handler import http_exception_handler

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/database/board", tags=["board"])

# -----------------------------------------------------
# 게시물 목록 조회 엔드포인트 정의
# -----------------------------------------------------
@router.get("/list",
            response_class=JSONResponse,
            response_model=BoardListResponse,
            # 특정값으로 세팅이 되지 않은 필드를 제거하고 응답을 보냄
            response_model_exclude_none=True,
            # 목록 내부 항목에서 특정 필드값을 제거하고 응답을 보낼때
            response_model_exclude={"boards": {"__all__": {"bdate", "bhitcount"}}})
async def list(board_service: BoardServiceDep, page_no: int = 1) -> BoardListResponse:
    # 페이징 대상이 되는 전체 행의 수를 DB에서 가져오기
    total_rows = await board_service.get_total_rows()

    # Pager 객체 생성
    pager = Pager.from_params(rows_per_page=10,
                              pages_per_group=5,
                              total_rows=total_rows,
                              page_no=page_no)
    
    # 해당 페이지의 게시물 가져오기
    list_board_entity = await board_service.list(pager)
    
    # BoardEntity 리스트 -> BoardListItemResponse 리스트로 변환
    list_board_list_item_response = [
        BoardListItemResponse.model_validate(board_entity) for board_entity in list_board_entity
    ]
    
    # BoardListResponse 생성
    board_list_response = BoardListResponse(pager=pager, boards=list_board_list_item_response)
    return board_list_response

@router.post("/create",
             response_class=JSONResponse,
             response_model=BoardResponse,
             response_model_exclude_none=True,
             response_model_exclude={"battachdata"})
async def create(
    board_write_request: Annotated[BoardWriteRequest, Form()],
    payload: LoginCheckDep,
    board_service: BoardServiceDep
) -> BoardResponse:
    logger.info("실행")
    
    # 첨부 파일 데이터 처리
    battach = board_write_request.battach
    battachoname = None
    battachtype = None
    battachdata = None
    if battach is not None and battach.filename:
        battachoname = battach.filename
        battachtype = battach.content_type
        battachdata = await battach.read()
    
    # BoardEntity 생성
    board_entity = BoardEntity(
        btitle = board_write_request.btitle,
        bcontent = board_write_request.bcontent,
        bwriter = payload.get("sub"),
        bdate = datetime.now(),
        battachoname = battachoname,
        battachtype = battachtype,
        battachdata = battachdata
    )
    
    # 데이터베이스에 저장 후 결과 반환
    board_entity = await board_service.create(board_entity)
    
    # Entity를 model로 변환하여 반환
    board_response = BoardResponse.model_validate(board_entity)
    return board_response

@router.get("/read/{bno}",
            response_class=JSONResponse,
            response_model=BoardResponse,
            response_model_exclude_none=True,
            response_model_exclude={"battachdata"})
async def read(
    payload: LoginCheckDep,
    board_service: BoardServiceDep,
    bno: int,
    caller: str | None = None,
):
    logger.info("실행")

    board_entity = await board_service.read(bno, bhitcount = (caller == "list"))

    if board_entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"게시물 번호 {bno}를 찾을 수 없습니다"
        )
        
    board_response = BoardResponse.model_validate(board_entity)
    return board_response

# ------------------------------------------------
# 첨부파일 다운로드 엔드포인트
# ------------------------------------------------
@router.get("/battach/{bno}", response_class=Response)
async def download(
    bno: int,
    board_service: BoardServiceDep
):
    logger.info("실행")
    
    # 게시물 조회
    board_entity = await board_service.read(bno)
    
    # 게시물이 존재하지 않으면 404 오류 반환
    if board_entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"게시물 번호 {bno}를 찾을 수 없습니다"
        )
    
    # 첨부파일 데이터가 존재하지 않으면 404 오류 반환
    if board_entity.battachdata is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"게시물 번호 {bno}에 첨부파일이 없습니다"
        )
    
    # Response로 파일 반환
    return Response(
        content=board_entity.battachdata, 
        media_type=board_entity.battachtype,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{board_entity.battachoname}"
        }
    )

@router.put("/update",
            response_class=JSONResponse,
            response_model=BoardResponse,
            response_model_exclude_none=True,
            response_model_exclude={"battachdata"})
async def update(
    board_update_request: Annotated[BoardUpdateRequest, Form()],
    payload: LoginCheckDep,
    board_service: BoardServiceDep
):
    logger.info("실행")
    
    battach = board_update_request.battach
    battachoname = None
    battachtype = None
    battachdata = None
    if battach is not None and battach.filename:
        battachoname = battach.filename
        battachtype = battach.content_type
        battachdata = await battach.read()
        
    board_entity = BoardEntity(
        bno = board_update_request.bno,
        btitle = board_update_request.btitle,
        bcontent = board_update_request.bcontent,
        battachoname = battachoname,
        battachtype = battachtype,
        battachdata = battachdata
    )
    
    board_entity = await board_service.modify(board_entity)
    
    board_response = BoardResponse.model_validate(board_entity)
    return board_response

@router.delete("/delete/{bno}")
async def remove(
    bno:int,
    payload: LoginCheckDep,
    board_service: BoardServiceDep
):
    logger.info("실행")
    success = await board_service.remove(bno)
    if success:
        return {"message": "게시물이 성공적으로 삭제되었습니다"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다")