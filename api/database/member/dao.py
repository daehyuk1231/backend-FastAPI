import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy import delete, text

from api.database.config.dbsession import OrmSessionDep
from api.database.member.entity import MemberEntity
from api.exception.handler import BusinessException

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
    
    # 회원 조회
    async def select_by_mid(self, mid: str) -> MemberEntity | None:
        member_entity = await self.orm_session.get(MemberEntity, mid)
        return member_entity
    
    # 회원 수정
    async def update(self, member_entity: MemberEntity) -> MemberEntity:
        # DB에 저장되어 있는 멤버 데이터 가져오기
        db_member_entity = await self.orm_session.get(MemberEntity, member_entity.mid)
        
        # 반드시 db_member_entity가 None 일 경우를 처리
        if db_member_entity is None:
            raise BusinessException("회원 아이디가 존재하지 않아 수정할 수 없음")
        
        # 수정해야할 부분을 찾아 세팅
        if member_entity.mpassword is not None:
            db_member_entity.mpassword = member_entity.mpassword
        if member_entity.menabled is not None:
            db_member_entity.menabled = member_entity.menabled
        if member_entity.memail is not None:
            db_member_entity.memail = member_entity.memail
        
        # 세션에서 수정된 내용을 DB에 반영할 때까지 대기
        await self.orm_session.flush()
        # DB에 반영된 내용을 다시 가져와서 db_member_entity 동기화
        await self.orm_session.refresh(db_member_entity)
        return db_member_entity
    
    # 회원 삭제
    async def delete_by_mid(self, mid: str) -> None:
        await self.orm_session.execute(
            delete(MemberEntity).where(MemberEntity.mid == mid)
        )
        # await self.orm_session.execute(
        #     text("DELETE FROM member WHERE mid=:mid"),
        #     {"mid":mid}
        # )
    
# ------------------------------------------------
# 의존성 타입 별칭 정의
# ------------------------------------------------
MemberDaoDep = Annotated[MemberDao, Depends(MemberDao)]