from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

# ========================
# Create New User
# ========================
def create_user(db: Session, user: schemas.UserCreate):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_pw = hash_password(user.password)

    # Create user model
    db_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_pw,
        bio=user.bio,
        avatar_url=user.avatar_url
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# ========================
# Authenticate User (Login)
# ========================
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None

    return user

# ========================
# Generate JWT Token
# ========================
def login_user(db: Session, login_data: schemas.UserLogin):
    user = authenticate_user(db, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create token
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ========================
# Get User Profile
# ========================
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ========================
# Update User Profile
# ========================
def update_user(db: Session, user_id: int, data: schemas.UserBase):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return None
    
    user.name = data.name
    user.bio = data.bio
    user.avatar_url = data.avatar_url
    
    db.commit()
    db.refresh(user)
    return user

# ========================
# Delete User
# ========================
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return True