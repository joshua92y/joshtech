# generated by datamodel-codegen:
#   filename:  OutstandingToken.json
#   timestamp: 2025-05-21T02:46:58+00:00

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OutstandingToken(BaseModel):
    id: Optional[int] = Field(None, title='id')
    user: Optional[int] = Field(None, title='user')
    jti: str = Field(..., title='jti')
    token: str = Field(..., title='token')
    created_at: Optional[datetime] = Field(None, title='created at')
    expires_at: datetime = Field(..., title='expires at')
