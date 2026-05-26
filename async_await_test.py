import asyncio

# 비동기(코루틴) 함수 정의
async def work1():
    print("비동기 작업1 시작")
    # 대기 -> 제어권을 이벤트 루프로 반환 -> 다른 비동기 작업 실행
    await asyncio.sleep(2)
    print("비동기 작업1 종료")

# 비동기(코루틴) 함수 정의
async def work2():
    print("비동기 작업2 시작")
    # 대기 -> 제어권을 이벤트 루프로 반환 -> 다른 비동기 작업 실행
    await asyncio.sleep(1)
    print("비동기 작업2 종료")
    
# 비동기(코루틴) 함수 정의
async def main():
    # 비동기 작업을 이벤트 루프에 등록
    task1 = asyncio.create_task(work1())
    task2 = asyncio.create_task(work2())
    # 대기 -> 제어권을 이벤트 루프로 반환 -> 다른 비동기 작업 실행
    await asyncio.sleep(0)
    # 비동기 작업 완료 대기
    await task1
    await task2
    
# 애플리케이션 시작: main() 실행
asyncio.run(main())