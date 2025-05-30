# generated by datamodel-codegen:
#   filename:  Session.json
#   timestamp: 2025-05-21T02:46:26+00:00

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Session(BaseModel):
    session_key: str = Field(..., title='세션 키')
    session_data: str = Field(..., title='세션 날짜')
    expire_date: datetime = Field(..., title='만료 날짜')
