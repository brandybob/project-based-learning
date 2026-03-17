from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    reg_number = Column(String(50), unique=True)
    
    assessments = relationship("Assessment", back_populates="student")
    feedbacks = relationship("Feedback", back_populates="student")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True)
    name = Column(String(100))
    lecturer_name = Column(String(100))

    assessments = relationship("Assessment", back_populates="unit")
    feedbacks = relationship("Feedback", back_populates="unit")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    type = Column(String(20)) # CAT 1, CAT 2, Assignment
    score = Column(Float)
    max_score = Column(Float, default=100.0)
    date_given = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="assessments")
    unit = relationship("Unit", back_populates="assessments")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    unit_id = Column(Integer, ForeignKey("units.id"))
    content = Column(String(500))
    teaching_rating = Column(Integer) # 1-5
    comments_on_lecturer = Column(String(500))
    date_submitted = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="feedbacks")
    unit = relationship("Unit", back_populates="feedbacks")
