import logging
from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from api.database.member.dao import MemberDaoDep
from api.database.member.entity import MemberEntity
from api.database.member.exception import MemberLoginError

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
    
    # 회원 로그인 비지니스 메소드
    async def login(self, mid: str, mpassword: str) -> MemberEntity:
        self.logger.info("실행")
        member_entity = await self.member_dao.select_by_mid(mid)
        if member_entity == None:
            raise MemberLoginError(
                message="회원 아이디가 존재하지 않음",
                error_code="A0006"
            )
        if not self.pwd_context.verify(mpassword, member_entity.mpassword):
            raise MemberLoginError(
                message="회원 비밀번호가 맞지 않음",
                error_code="A0006"
            )
        return member_entity
        
# ------------------------------------------------
# 의존성 타입 별칭 정의
# ------------------------------------------------
MemberServiceDep = Annotated[MemberService, Depends(MemberService)]