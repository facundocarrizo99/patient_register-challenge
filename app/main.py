from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import os
import imghdr
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

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

    # Validate file type
    if not document_photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    # Validate file size (max 5MB)
    contents = await document_photo.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB).")
    # Optionally check file signature
    if imghdr.what(None, h=contents) not in ["jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are allowed.")
    # Reset file pointer for saving
    document_photo.file.seek(0)

    # Save uploaded file
    file_ext = os.path.splitext(document_photo.filename)[1]
    file_name = f"{email.replace('@', '_at_')}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(await document_photo.read())

    # Store patient in DB
    try:
        patient = crud.create_patient(db, patient_in, document_photo_path=file_path)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error.")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error.")

    # Send confirmation email asynchronously
    background_tasks.add_task(email_utils.send_confirmation_email, email, name)

    return patient

@app.get("/")
def root():
    return {"message": "Patient Registration API"} 