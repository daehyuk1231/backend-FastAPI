import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.database.board.model import BoardListItemResponse, BoardListResponse, Pager
from api.database.board.service import BoardServiceDep

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