from datetime import datetime
import logging
from typing import Annotated

from fastapi import Depends

from api.di.dao import MemberDaoDep

# ----------------------------------
# 회원 서비스 클래스
# ----------------------------------
class MemberService:
    def __init__(self, memberDao: MemberDaoDep) -> None:
        self.logger = logging.getLogger(f"{__name__}.MemberService")
        self.memberDao = memberDao
    
    def get_member(self) -> dict:
        self.logger.info("get_member() 실행")
        member = self.memberDao.select()
        return member
    
    def join(self) -> dict:
        member = self.memberDao.insert()
        return member

MemberServiceDep = Annotated[MemberService, Depends(MemberService)]
        
# 모듈 싱글톤 생성
# member_service_instance = MemberService()
# def get_member_service() -> MemberService:
#     return member_service_instance
# MemberServiceDep = Annotated[MemberService, Depends(get_member_service)]