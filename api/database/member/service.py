import logging
from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from api.database.member.dao import MemberDaoDep
from api.database.member.entity import MemberEntity

class MemberService:
    def __init__(self, member_dao: MemberDaoDep) -> None:
        self.logger = logging.getLogger(f"{__name__}.MemberService")
        self.member_dao = member_dao
        self.pwd_context = CryptContext(schemes=["bcrypt"])
    
    # 회원 가입 비지니스 메소드
    async def join(self, member_entity: MemberEntity) -> MemberEntity:
        self.logger.info("실행")
        # 패스워드 암호화
        member_entity.mpassword = self.pwd_context.hash(member_entity.mpassword)
        # DAO를 이용해서 DB에 저장
        member_entity = await self.member_dao.insert(member_entity)
        return member_entity
        
# ------------------------------------------------
# 의존성 타입 별칭 정의
# ------------------------------------------------
MemberServiceDep = Annotated[MemberService, Depends(MemberService)]