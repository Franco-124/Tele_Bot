from pydantic import BaseModel

class RequestModel(BaseModel):
    message: str

class AnswerModel(BaseModel):
    answer: str

class ErrorModel(BaseModel):
    error: str