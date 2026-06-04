from datetime import datetime
from typing import Self

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

# ------------------------------------------
# Pager 모델 클래스 정의
# ------------------------------------------
class Pager(BaseModel):
    total_rows: int         # "전체 데이터 수"
    total_page_no: int      # "전체 페이지 수"
    total_group_no: int     # "전체 그룹 수"
    start_page_no: int      # "시작 페이지 번호"
    end_page_no: int        # "끝 페이지 번호"
    page_array: list[int]   # "페이지 배열"
    page_no: int            # "현재 페이지 번호"
    pages_per_group: int    # "그룹당 페이지 수"
    group_no: int           # "현재 그룹 번호"
    rows_per_page: int      # "페이지당 데이터 수"
    start_row_no: int       # "시작 데이터 번호"
    start_row_index: int    # "시작 데이터 인덱스"
    end_row_no: int         # "끝 데이터 번호"
    end_row_index: int      # "끝 데이터 인덱스"
    
    @classmethod
    def from_params(cls, 
                    rows_per_page: int,
                    pages_per_group: int,
                    total_rows: int,
                    page_no: int) -> Self:
        # 주어진 갑이외에 나머지 값들을 계산
        total_page_no = total_rows // rows_per_page
        if total_rows % rows_per_page != 0:
            total_page_no += 1

        total_group_no = 0
        if total_page_no > 0:
            total_group_no = total_page_no // pages_per_group
            if total_page_no % pages_per_group != 0:
                total_group_no += 1

        group_no = (page_no - 1) // pages_per_group + 1
        if total_group_no == 0:
            group_no = 0

        start_page_no = (group_no - 1) * pages_per_group + 1 if group_no > 0 else 0
        end_page_no = start_page_no + pages_per_group - 1 if group_no > 0 else 0
        if group_no == total_group_no and total_group_no > 0:
            end_page_no = total_page_no

        if start_page_no and start_page_no <= end_page_no:
            page_array = list(range(start_page_no, end_page_no + 1))
        else:
            page_array = []

        start_row_no = (page_no - 1) * rows_per_page + 1
        start_row_index = start_row_no - 1
        end_row_no = page_no * rows_per_page
        end_row_index = end_row_no - 1
        
        # 생성자를 호출하고 객체를 반환
        return cls(
            rows_per_page=rows_per_page,
            pages_per_group=pages_per_group,
            total_rows=total_rows,
            page_no=page_no,
            total_page_no=total_page_no,
            total_group_no=total_group_no,
            group_no=group_no,
            start_page_no=start_page_no,
            end_page_no=end_page_no,
            page_array=page_array,
            start_row_no=start_row_no,
            start_row_index=start_row_index,
            end_row_no=end_row_no,
            end_row_index=end_row_index,
        )
        
# -----------------------------------------------------
# 하나의 게시물을 저장하는 모델 클래스 정의
# -----------------------------------------------------
class BoardListItemResponse(BaseModel):
    bno: int
    btitle: str
    bwriter: str
    bdate: datetime
    bhitcount: int
    battachoname: str | None = None
    battachtype: str | None  = None
    model_config = ConfigDict(from_attributes=True) # 엔티티로 dto 자동 생성
    
# -----------------------------------------------------
# 게시물 목록 모델 클래스 정의
# -----------------------------------------------------
class BoardListResponse(BaseModel):
    pager: Pager
    boards: list[BoardListItemResponse]
    
# ------------------------------------------------
# 게시물 쓰기 요청용 모델
# ------------------------------------------------
class BoardWriteRequest(BaseModel):
    btitle: str
    bcontent: str | None = None
    battach: UploadFile | None  = None

# ------------------------------------------------
# 게시물 상세 조회용 모델 (대용량 필드 포함)
# ------------------------------------------------
class BoardResponse(BaseModel):
    bno: int
    btitle: str
    bcontent: str | None = None
    bwriter: str
    bdate: datetime
    bhitcount: int
    battachoname: str | None = None
    battachsname: str | None = None
    battachtype: str | None = None
    battachdata: bytes | None = None    
    model_config = ConfigDict(from_attributes=True)
    
class BoardUpdateRequest(BaseModel):
    bno: int
    btitle: str
    bcontent: str | None = None
    battach: UploadFile | None = None