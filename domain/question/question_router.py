from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud

from starlette import status

# create test
from models import Question
from datetime import datetime

router = APIRouter(
    prefix="/api/question",
)


@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _question_list = question_crud.get_question_list(db, skip=page*size, limit=size)

    return {
        'total': total,
        'question_list': _question_list
    }


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=201)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    question_crud.create_question(db=db, question_create=_question_create)

@router.get("/test_data",status_code=201)
def test_data_create(db: Session = Depends(get_db)):

    for i in range(300):
        _question_create = Question(subject='테스트 데이터입니다:[%03d]' % i, content='테스트', create_date=datetime.now())
        question_crud.create_question(db=db, question_create=_question_create)