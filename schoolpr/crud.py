from sqlalchemy.orm import Session
from . import models, schemas

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_assessment(db: Session, assessment: schemas.AssessmentCreate):
    db_assessment = models.Assessment(**assessment.model_dump())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_units(db: Session):
    return db.query(models.Unit).all()

def create_unit(db: Session, unit: schemas.UnitCreate):
    db_unit = models.Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit

def get_student_performance(db: Session, student_id: int):
    # Logic to calculate average and give recommendations
    assessments = db.query(models.Assessment).filter(models.Assessment.student_id == student_id).all()
    if not assessments:
        return {"average": 0, "recommendations": []}
    
    total_score = sum([a.score / a.max_score for a in assessments])
    count = len(assessments)
    average = (total_score / count) * 100

    recommendations = []
    if average < 50:
        recommendations.append({
            "type": "peer_tutor",
            "message": "Your score is below 50%. We recommend joining a peer tutoring group for this unit."
        })
        recommendations.append({
            "type": "online_resource",
            "message": "Check out this foundational course on YouTube.",
            "link": "https://www.youtube.com/results?search_query=educational+basics"
        })
    elif average < 70:
        recommendations.append({
            "type": "study_partner",
            "message": "You're doing okay! Finding a study partner might help you reach the next level."
        })
    else:
        recommendations.append({
            "type": "online_resource",
            "message": "Great job! Here's some advanced reading to keep you ahead.",
            "link": "https://scholar.google.com"
        })

    return {"average": round(average, 2), "recommendations": recommendations}
