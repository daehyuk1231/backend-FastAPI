from api.database.config.entity_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, Integer, LargeBinary, String, Text
from datetime import datetime

class BoardEntity(Base):
    __tablename__ = "board"
    bno: Mapped[int] = mapped_column("bno", Integer, primary_key=True, autoincrement=True)
    btitle: Mapped[str] = mapped_column("btitle", String(255))
    bcontent: Mapped[str | None] = mapped_column("bcontent", Text)
    bwriter: Mapped[str] = mapped_column("bwriter", String(50), ForeignKey("member.mid"))
    bdate: Mapped[datetime] = mapped_column("bdate", DateTime())
    bhitcount: Mapped[int] = mapped_column("bhitcount", Integer, server_default="0")
    battachoname: Mapped[str | None] = mapped_column("battachoname", String(255))
    battachsname: Mapped[str | None] = mapped_column("battachsname", String(255))
    battachtype: Mapped[str | None] = mapped_column("battachtype", String(255))
    battachdata: Mapped[bytes | None] = mapped_column("battachdata", LargeBinary)