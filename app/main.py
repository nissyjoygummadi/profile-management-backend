from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, get_db
from . import models, schemas, crud

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Profile Management Service")

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # (later you can restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Health Check Route
# ============================
@app.get("/")
def health():
    return {"status": "ok", "message": "Backend is running"}

# ============================
# Register User
# ============================
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# ============================
# Login
# ============================
@app.post("/login")
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db, login_data)

# ============================
# Get Profile
# ============================
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ============================
# Update Profile
# ============================
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_profile(user_id: int, data: schemas.UserBase, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ============================
# Delete Profile
# ============================
@app.delete("/users/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    result = crud.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted": True}