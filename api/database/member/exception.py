class MemberLoginError(Exception):
    def __init__(self, 
                 message: str | None = None,
                 error_code: str | None = None) -> None:
        self.error_code = error_code    # A0003 (비지니스 로직 상의 에러 코드)
        super().__init__(message)