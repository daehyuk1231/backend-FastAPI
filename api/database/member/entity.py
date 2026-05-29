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