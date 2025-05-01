# backend-api/app/routers/contact.py

from fastapi import APIRouter, Body
from Contactmessage import ContactMessage
from backend_admin.contact.models import ContactMessage as DjangoContact

router = APIRouter()


@router.post(
    "/contact",
    response_model=ContactMessage,
    summary="문의 메시지 제출",
    description="사용자로부터 문의 메시지를 수신합니다.",
    response_description="제출된 메시지 반환",
)
def submit_contact(msg: ContactMessage):
    DjangoContact.objects.create(name=msg.name, email=msg.email, message=msg.message)
    return msg
