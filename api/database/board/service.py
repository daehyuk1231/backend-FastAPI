import logging
from typing import Annotated

from fastapi import Depends

from api.database.board.dao import BoardDaoDep
from api.database.board.entity import BoardEntity
from api.database.board.model import Pager

# -----------------------------------------------
# BoardService 클래스 정의
# -----------------------------------------------
class BoardService:
    def __init__(self, board_dao: BoardDaoDep) -> None:
        self.logger = logging.getLogger(f"{__name__}.BoardService")
        self.board_dao = board_dao
        
    # 페이징 대상이 되는 전체 행의 수를 얻기
    async def get_total_rows(self) -> int:
        total_count = await self.board_dao.select_count()
        return total_count
    
    # 해당 페이지의 게시물 목록 가져오기
    async def list(self, pager: Pager) -> list[BoardEntity]:
        list_board_entity = await self.board_dao.select_by_page(pager)
        return list_board_entity

    # async def list(self, pager: Pager) -> list[dict]:
    #     list_board_entity = await self.board_dao.select_by_page(pager)
    #     return list_board_entity
    
    # 게시물 쓰기
    async def create(self, board_entity: BoardEntity) -> BoardEntity:
        self.logger.info("실행")
        board_entity = await self.board_dao.insert(board_entity)
        return board_entity
    
    async def read(self, bno:int, bhitcount: bool = False) -> BoardEntity | None:
        self.logger.info("실행")
        board_entity = await self.board_dao.select_by_bno(bno)
        if bhitcount and board_entity is not None:
            board_entity = await self.board_dao.update_hitcount(board_entity)
        return board_entity
    
    async def modify(self, board_entity: BoardEntity) -> BoardEntity:
        self.logger.info("실행")
        board_entity = await self.board_dao.update(board_entity)
        return board_entity
    
    async def remove(self, bno: int) -> bool:
        self.logger.info("실행")
        return await self.board_dao.delete_by_bno(bno)
    
# -----------------------------------------------
# 의존성 타입 별칭 정의
# -----------------------------------------------
BoardServiceDep = Annotated[BoardService, Depends(BoardService)]