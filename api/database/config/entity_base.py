from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# 엔티티 클래스의 부모 클래스 정의
# - AsyncAttrs와 DeclarativeBase를 상속
# - AsyncAttrs: SQLAlchemy의 비동기 ORM 기능을 제공하는 클래스
# - DeclarativeBase: SQLAlchemy의 선언적 매핑 기능을 제공하는 클래스
class Base(AsyncAttrs, DeclarativeBase):
    pass