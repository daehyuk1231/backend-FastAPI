import logging
from typing import Annotated

from fastapi import Depends

from api.database.config.dbsession import OrmSessionDep
from api.database.member.entity import MemberEntity

class MemberDao:
    def __init__(self, orm_session: OrmSessionDep) -> None:
        self.logger = logging.getLogger(f"{__name__}.MemberDao")
        self.orm_session = orm_session
        
    # 회원 등록
    async def insert(self, member_entity: MemberEntity) -> MemberEntity:
        self.logger.info("실행")
        # 세션을 이용해서 새 회원 저장
        self.orm_session.add(member_entity)
        # DB에 완전히 저장될때까지 기다림
        await self.orm_session.flush()
        # DB에 저장된 회원 정보 가져오기
        await self.orm_session.refresh(member_entity)
        # 저장된 회원 정보를 반환
        return member_entity
        
# ------------------------------------------------
# 의존성 타입 별칭 정의
# ------------------------------------------------
MemberDaoDep = Annotated[MemberDao, Depends(MemberDao)]