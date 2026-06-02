import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy import func, select, text
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
                # bno를 기준으로 내림차순 정렬
                .order_by(BoardEntity.bno)
                # 페이징 처리
                .limit(pager.rows_per_page)
                .offset(pager.start_row_index)
        )
        
        # result = await self.orm_session.execute(
        #     text("""
        #         SELECT bno, btitle, bwriter, bdate, bhitcount, battachoname, battachtype 
        #         FROM board 
        #         ORDER BY bno DESC 
        #         LIMIT :limit OFFSET :offset
        #         """),
        #     {"limit": pager.rows_per_page, "offset": pager.start_row_index}
        # )
        
        return list(result.scalars().all())
        
# -----------------------------------------------
# 의존성 타입 별칭 정의
# -----------------------------------------------
BoardDaoDep = Annotated[BoardDao, Depends(BoardDao)]