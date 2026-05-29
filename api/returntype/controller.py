from datetime import datetime
import logging
import mimetypes
from pathlib import Path
from urllib.parse import quote
from fastapi import APIRouter, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from api.returntype.model import BoardResponse
from dicttoxml import dicttoxml

# 로거 생성
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(prefix="/return-type", tags=["return-type"])

# 템플릿 객체 얻기
templates = Jinja2Templates("templates")

# 엔드포인트 정의


@router.get("/string", response_class=PlainTextResponse)
async def return_string():
    return "success"


@router.get("/html", response_class=HTMLResponse)
async def return_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/model",
            response_class=JSONResponse,
            response_model=BoardResponse,
            response_model_exclude_none=True)
async def return_model():
    board_response = BoardResponse(
        bno=1,
        btitle="게시글 제목",
        bcontent="게시물 내용",
        bwriter="user",
        bhitcount=1,
        bdate=datetime.now(),
        battachoname="photo1.jpg",
    )
    return board_response


@router.get("/list",
            response_class=JSONResponse,
            response_model=list[BoardResponse],
            response_model_exclude_unset=True)
async def return_list():
    board_list = []
    for i in range(1, 4):
        board_response = BoardResponse(
            bno=1,
            btitle="게시글 제목",
            bcontent="게시물 내용",
            bwriter="user",
            bhitcount=1,
            bdate=datetime.now()
        )
        board_list.append(board_response)
    return board_list


@router.get("/xml",
            response_class=Response)
async def return_xml():
    board_list = []
    for i in range(1, 4):
        board_response = BoardResponse(
            bno=1,
            btitle="게시글 제목",
            bcontent="게시물 내용",
            bwriter="user",
            bhitcount=1,
            bdate=datetime.now()
        )
        # BoardResponse -> dict
        board_dict = board_response.model_dump(exclude_none=True)
        board_list.append(board_dict)

    # dict -> xml 변환
    xml_data = dicttoxml(board_list, custom_root="boards", attr_type=False)

    # 응답 생성
    return Response(
        content=xml_data,
        media_type="application/xml"
    )


@router.get("/status-code",
            response_class=JSONResponse,
            response_model=BoardResponse | None)
async def return_status_code(response: Response):
    if True:
        board_response = BoardResponse(
            bno=1,
            btitle="게시글 제목",
            bcontent="게시물 내용",
            bwriter="user",
            bhitcount=1,
            bdate=datetime.now()
        )
        return board_response
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

# 파일 시스템에 있는 파일을 다운로드할 경우
@router.get("/file", response_class=FileResponse)
async def return_file():
    file_name = "사진1.jpg"
    save_dir = Path.home() / "Desktop" / "kosa-course" / "temp"
    file_path = save_dir / file_name
    media_type, _ = mimetypes.guess_type(file_path)
    # mime_type, _ = ('image/jpeg', None)

    # 한글 파일을 UTF-8 문자셋으로 인코딩
    # 한글 1자는 3바이트: 3바이트로 해석해서 16진수로 변경한 알파벳으로 변환
    file_encoded_name = quote(file_name)
    logger.info("file_encoded_name:", file_encoded_name)

    return FileResponse(
        path=file_path,
        media_type=media_type,
        headers={
            # HTTP 헤더에는 ISO-8859_1 타입의 문자들만 들어가야함.(영어, 숫자, 라틴어, 일부 특수문자)
            "Content-Disposition": f"attachment; filename*=UTF-8''{file_encoded_name}"
        }
    )

# DB에 있는 파일을 다운로드할 경우
@router.get("/file-db", response_class=Response)
async def return_file_db():
    # DB에서 읽은 데이터
    battachoname = "사진1.jpg"
    battachtype = "image/jpeg"
    battachdata = "..." # bytes 데이타
    
    save_dir = Path.home() / "Desktop" / "kosa-course" / "temp"
    file_path = save_dir / battachoname
    with open(file_path, "br") as file:
        battachdata = file.read()
    
    # 한글 파일을 UTF-8 문자셋으로 인코딩
    # 한글 1자는 3바이트: 3바이트로 해석해서 16진수로 변경한 알파벳으로 변환
    file_encoded_name = quote(battachoname)
    logger.info("file_encoded_name:", file_encoded_name)

    return Response(
        content=battachdata,
        media_type=battachtype,
        headers={
            # HTTP 헤더에는 ISO-8859_1 타입의 문자들만 들어가야함.(영어, 숫자, 라틴어, 일부 특수문자)
            "Content-Disposition": f"attachment; filename*=UTF-8''{file_encoded_name}"
        }
    )