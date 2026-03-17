from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

# Absolute imports
from schoolpr import crud, models, schemas
from schoolpr.database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# Initialize Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    path = os.path.join("schoolpr", "form.html")
    if not os.path.exists(path):
        path = "form.html"
    return FileResponse(path)

@app.post("/feedback/", response_model=schemas.Feedback)
def create_assessment(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return crud.create_feedback(db=db, feedback=feedback)

# --- REFINED SMART GROUPING LOGIC ---
@app.get("/groups/{unit_id}")
def get_assessment_groups(unit_id: int, db: Session = Depends(get_db)):
    """
    Categorizes students specifically for Peer-to-Peer support.
    80+  -> Mentors (Can teach others)
    50-79 -> Study Partners (Can collaborate)
    <50  -> Need Support (The ones who see the matches)
    """
    all_records = db.query(models.Feedback).filter(models.Feedback.unit_id == unit_id).all()
    
    # Advanced students are suggested as Mentors
    mentors = [f"Student {r.student_id}" for r in all_records if r.teaching_rating >= 80]
    
    # Intermediate students are suggested as Study Partners
    partners = [f"Student {r.student_id}" for r in all_records if 50 <= r.teaching_rating < 80]
    
    # Beginner students (For the Lecturer's intervention list)
    struggling = [f"Student {r.student_id}" for r in all_records if r.teaching_rating < 50]
    
    return {
        "unit_id": unit_id,
        "advanced": mentors,      # Frontend calls these "Recommended Tutors"
        "intermediate": partners,  # Frontend calls these "Study Partners"
        "beginner": struggling,
        "total_count": len(all_records)
    }

@app.get("/all_feedback/", response_model=List[schemas.Feedback])
def get_all_feedback(db: Session = Depends(get_db)):
    """Lecturer Dashboard Data"""
    return db.query(models.Feedback).all()