from resume import ResumeSchema

def sample_resume():
    return ResumeSchema(
        name="홍길동",
        email="hong@example.com",
        phone="010-1234-5678",
        summary="파이썬 백엔드 개발자"
    )