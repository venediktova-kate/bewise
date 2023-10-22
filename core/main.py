from datetime import datetime
from typing import List

import requests
from fastapi import FastAPI, status, Depends

from database import SessionLocal
from models import Quiz
from schemas import CreateQuiz
from sqlalchemy.orm import Session

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=List[CreateQuiz], status_code=status.HTTP_200_OK)
def get_display(db: Session = Depends(get_db)):
    data_db = [
        {
            'id': i.id,
            'id_question': i.id_question,
            'question': i.question,
            'answer': i.answer,
            'created_at': (datetime.strftime(i.created_at, "%Y-%m-%dT%H:%M:%S.%fZ"))

        }

        for i in db.query(Quiz).all()[:-1]
    ]

    return [CreateQuiz(**row) for row in data_db]


@app.post("/", status_code=status.HTTP_201_CREATED)
def get_create(count: int, db: Session = Depends(get_db)) -> None:
    url = f'https://jservice.io/api/random?count={count}'
    response_data = requests.get(url).json()

    for items in response_data:
        while db.query(Quiz).filter(Quiz.id_question is items['id']).first() is not None:
            items = requests.get(
                url=f"https://jservice.io/api/random?count=1"
            ).json()
            print('True')

        answer_db = Quiz(
            id_question=items["id"],
            question=items["question"],
            answer=items["answer"],
            created_at=items['created_at']

        )
        db.add(answer_db)
        db.commit()
        db.refresh(answer_db)
