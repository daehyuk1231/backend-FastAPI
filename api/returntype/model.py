from datetime import datetime
from pydantic import BaseModel


class BoardResponse(BaseModel):
    bno: int
    btitle: str
    bcontent: str
    bwriter: str
    bdate: datetime
    bhitcount: int
    battachoname: str | None = None
    battachsname: str | None = None
    battachtype: str | None = None