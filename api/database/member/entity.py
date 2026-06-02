from sqlalchemy import Boolean, String

from api.database.config.entity_base import Base
from sqlalchemy.orm import Mapped, mapped_column

class MemberEntity(Base):
    __tablename__ = "member"
    mid: Mapped[str] = mapped_column(String(20), primary_key=True)
    mname: Mapped[str] = mapped_column(String(20))
    mpassword: Mapped[str] = mapped_column(String(255))
    memail: Mapped[str] = mapped_column(String(255))
    menabled: Mapped[bool] = mapped_column(Boolean)
    mrole: Mapped[str] = mapped_column(String(20))
    
'''
SQLAlchemy가 자동 생성하는 DDL

-- Oracle
CREATE TABLE member (
    mid       VARCHAR2(20)   PRIMARY KEY,
    mname     VARCHAR2(20)  NOT NULL,
    mpassword VARCHAR2(255)  NOT NULL,
    memail    VARCHAR2(255)  NOT NULL UNIQUE,
    menabled  NUMBER(1)      NOT NULL,
    mrole     VARCHAR2(20)   NOT NULL
)

-- PostgreSQL
CREATE TABLE member (
    mid       VARCHAR(20)   PRIMARY KEY,
    mname     VARCHAR(20)  NOT NULL,
    mpassword VARCHAR(255)  NOT NULL,
    memail    VARCHAR(255)  NOT NULL UNIQUE,
    menabled  BOOLEAN       NOT NULL,
    mrole     VARCHAR(20)   NOT NULL
)
'''