from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AssessmentBase(BaseModel):
    unit_id: int
    type: str
    score: float
    max_score: float = 100.0

class AssessmentCreate(AssessmentBase):
    student_id: int

class Assessment(AssessmentBase):
    id: int
    student_id: int
    date_given: datetime

    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    unit_id: int
    content: str
    teaching_rating: int
    comments_on_lecturer: str

class FeedbackCreate(FeedbackBase):
    student_id: int

class Feedback(FeedbackBase):
    id: int
    student_id: int
    date_submitted: datetime

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    email: str
    reg_number: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    assessments: List[Assessment] = []
    feedbacks: List[Feedback] = []

    class Config:
        from_attributes = True

class UnitBase(BaseModel):
    code: str
    name: str
    lecturer_name: str

class UnitCreate(UnitBase):
    pass

class Unit(UnitBase):
    id: int

    class Config:
        from_attributes = True

class Recommendation(BaseModel):
    type: str # "peer_tutor", "study_partner", "online_resource"
    message: str
    link: Optional[str] = None


class FeedbackCreate(BaseModel):
    student_id: int
    unit_id: int
    content: str
    teaching_rating: int  # This is our assessment score
    comments_on_lecturer: str