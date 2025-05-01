# portfolio\apps\backend-admin\resume\pydantic_models.py
from djantic import ModelSchema
from resume.models import Resume

class ResumeSchema(ModelSchema):
    class Config:
        model = Resume
