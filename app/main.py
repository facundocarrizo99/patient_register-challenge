from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import os
from . import models, schemas, crud, database, email_utils

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients", response_model=schemas.PatientOut)
async def register_patient(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    document_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate input using Pydantic
    patient_in = schemas.PatientCreate(name=name, email=email, phone=phone)

    # Check if email already exists
    if db.query(models.Patient).filter(models.Patient.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Save uploaded file
    file_ext = os.path.splitext(document_photo.filename)[1]
    file_name = f"{email.replace('@', '_at_')}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(await document_photo.read())

    # Store patient in DB
    patient = crud.create_patient(db, patient_in, document_photo_path=file_path)

    # Send confirmation email asynchronously
    background_tasks.add_task(email_utils.send_confirmation_email, email, name)

    return patient

@app.get("/")
def root():
    return {"message": "Patient Registration API"} 