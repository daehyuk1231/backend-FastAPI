from datetime import datetime
import logging
from typing import Annotated

from fastapi import Depends

# 클래스 정의
class MemberDao:
    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.MemberDao")
        
    def select(self) -> dict:
        self.logger.info("select() 실행")
        return {
            "mid": "hong",
            "mname": "홍길동",
            "memail": "hong@mycompany.com"
        }
        
    def insert(self) -> dict:
        return {
            "mid": "hong",
            "mname": "홍길동",
            "memail": "hong@mycompany.com",
            "mdate": datetime.now()
        }

# 의존성 타입 별칭 정의        
MemberDaoDep = Annotated[MemberDao, Depends(MemberDao)]