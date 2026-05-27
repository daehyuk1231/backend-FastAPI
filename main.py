from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


# ============================================
# FastAPI 애플리케이션 인스턴스 생성
# ============================================
app = FastAPI(
    title="FastAPI 백엔드",
    description="FastAPI를 학습하기 위한 프로젝트",
    version="1.0.0"
)

# ============================================
# 정적 파일 디렉토리 설정
# ============================================
# 정적 파일을 요청할때 사용할 URL 경로 설정
# 정적 파일을 저장하는 디렉토리를 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# ============================================
# 템플릿 디렉토리 설정
# ============================================
# 템플릿 엔진으로 Jinja2를 사용
# View(HTML)을 생성하는 동적 파일을 저장할 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# ============================================
# 홈(/) 라우트(엔드포인트) 설정
# ============================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # TemplateResponse() 메소드는 HTMLResponse 객체를 반환
    return templates.TemplateResponse("index.html", {"request":request})

# ============================================
# 애플리케이션 시작
# ============================================
if __name__ == "__main__":
    uvicorn.run(
        # 유비콘(비동기 서버)가 실행할 애플리케이션
        # reload=False일 경우: app을 제공할 수 있음
        # reload=True 일 경우: "main:app"과 같이 문자열로 제공해야 함
        # main 모듈을 찾아 app을 재시작해야 하므로 모듈 이름이 필요
        "main:app",         
        host="localhost",   # 0.0.0.0은 모든 네트워크 인터페이스에서 접근 가능
        port=8000,            # 서버가 실행될 포트 번호     
        reload=True,        # 코드 변경 시 자동으로 서버를 재시작
        access_log=True,    # HTTP 요청/응답 접근 로그 활성화
    )