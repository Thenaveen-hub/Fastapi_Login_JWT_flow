from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, auth_handler
from database import engine, get_db
from typing import List

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/signup", response_model=schemas.Token)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and save
    hashed_pass = auth_handler.get_password_hash(user.password)
    new_user = models.User(fullname=user.fullname, email=user.email, hashed_password=hashed_pass)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return auth_handler.signJWT(new_user.email)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Query user by email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    # Verify existence and password hash
    if not db_user or not auth_handler.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return auth_handler.signJWT(db_user.email)

# ... (existing imports)

# In main.py
@app.get("/users", tags=["Admin"])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.put("/user/change-password", tags=["User Settings"])
def change_password(
    email: str, 
    current_password: str, 
    new_password: str, 
    db: Session = Depends(get_db)
):
    """
    Standard Change Password mechanism.
    Verifies the current password before updating the SQLite database with the new hash.
    """
    # 1. Fetch the user from SQLite
    db_user = db.query(models.User).filter(models.User.email == email).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Verify the old password using the auth_handler fix
    if not auth_handler.verify_password(current_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # 3. Hash the new password and update the record
    db_user.hashed_password = auth_handler.get_password_hash(new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}

@app.delete("/user/delete/{user_id}", tags=["Admin"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a specific user from the SQLite database by their ID.
    Useful for manual testing to reset your user list.
    """
    # 1. Search for the user in the database
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    
    # 2. If user doesn't exist, raise 404
    if not user_to_delete:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # 3. Delete and save changes
    db.delete(user_to_delete)
    db.commit()
    
    return {"message": f"User {user_id} has been successfully deleted"}