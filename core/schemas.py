from datetime import datetime

from pydantic import BaseModel


class CreateQuiz(BaseModel):
    id: int
    id_question: int
    question: str
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True
