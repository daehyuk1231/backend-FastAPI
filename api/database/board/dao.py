import logging
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import delete, func, select, text
from sqlalchemy.orm import load_only

from api.database.board.entity import BoardEntity
from api.database.board.model import Pager
from api.database.config.dbsession import OrmSessionDep

# -----------------------------------------------
# BoardDao 클래스 정의
# -----------------------------------------------
class BoardDao:
    def __init__(self, orm_session: OrmSessionDep) -> None:
        self.logger = logging.getLogger(f"{__name__}.BoardDao")
        self.orm_session = orm_session
        
    # 페이징 대상이되는 전체 행의 수 조회
    async def select_count(self) -> int:
        result = await self.orm_session.execute(
            select(func.count(BoardEntity.bno))
                .where(BoardEntity.bno <= 50)
        )
        # result = await self.orm_session.execute(
        #     text("SELECT COUNT(bno) FROM board")
        # )
        rows = result.scalar()
        if rows is None:
            return 0
        else:
            return rows
        
    # 해당 페이지의 게시물 목록 조회하기
    async def select_by_page(self, pager: Pager) -> list[BoardEntity]:
        result = await self.orm_session.execute(
            select(BoardEntity)
                # 필요한 컬럼만 가져오기
                .options(
                    load_only(
                        BoardEntity.bno,
                        BoardEntity.btitle,
                        BoardEntity.bwriter,
                        BoardEntity.bdate,
                        BoardEntity.bhitcount,
                        BoardEntity.battachoname,
                        BoardEntity.battachtype,
                    )
                )
                .where(BoardEntity.bno <= 50)
                # bno를 기준으로 내림차순 정렬
                .order_by(BoardEntity.bno.desc())
                # 페이징 처리
                .limit(pager.rows_per_page)
                .offset(pager.start_row_index)
        )
        return list(result.scalars().all())
    
    # async def select_by_page(self, pager: Pager) -> list[dict[str, Any]]:
    #     result = await self.orm_session.execute(
    #         text("""
    #             SELECT bno, btitle, bwriter, bdate, bhitcount, battachoname, battachtype 
    #             FROM board 
    #             ORDER BY bno DESC 
    #             LIMIT :limit OFFSET :offset
    #             """), 
    #         {"limit": pager.rows_per_page, "offset": pager.start_row_index}
    #     )

    #     # RowMapping 객체를 일반 dict로 변환해서 상위 계층에서 DTO로 명시 매핑한다.
    #     return [dict(row) for row in result.mappings().all()]
    
    async def insert(self, entity: BoardEntity) -> BoardEntity:
        self.logger.info("실행")
        self.orm_session.add(entity)
        
        await self.orm_session.flush()
        await self.orm_session.refresh(entity)
        return entity
    
    async def select_by_bno(self, bno: int) -> BoardEntity | None:
        self.logger.info("실행")
        board_entity = await self.orm_session.get(BoardEntity, bno)
        return board_entity
    
    async def update_hitcount(self, board_entity: BoardEntity) -> BoardEntity:
        self.logger.info("실행")
        board_entity.bhitcount += 1
        await self.orm_session.flush()
        return board_entity
    
    async def update(self, entity: BoardEntity) -> BoardEntity:
        self.logger.info("실행")

        db_board_entity = await self.orm_session.get(BoardEntity, entity.bno)
        
        if db_board_entity is None:
            raise Exception("게시글을 찾을 수 없습니다.")
        
        if entity.btitle is not None:
            db_board_entity.btitle = entity.btitle
        
        if entity.bcontent is not None:
            db_board_entity.bcontent = entity.bcontent
            
        if entity.battachoname is not None:
            db_board_entity.battachoname = entity.battachoname
            db_board_entity.battachsname = entity.battachsname
            db_board_entity.battachtype = entity.battachtype
            db_board_entity.battachdata = entity.battachdata
            
        await self.orm_session.flush()
        await self.orm_session.refresh(db_board_entity)
        
        return db_board_entity
    
    async def delete_by_bno(self, bno: int) -> bool:
        self.logger.info("실행")
        
        # board_entity = await self.orm_session.get(BoardEntity, bno)
        # if board_entity:
        #     await self.orm_session.delete(board_entity)
        #     return True
        # else:
        #     return False
        
        result = await self.orm_session.execute(
            delete(BoardEntity).where(BoardEntity.bno == bno)
        )
        return result.rowcount > 0
            
# -----------------------------------------------
# 의존성 타입 별칭 정의
# -----------------------------------------------
BoardDaoDep = Annotated[BoardDao, Depends(BoardDao)]