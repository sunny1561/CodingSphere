
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from mongoengine import connect, ValidationError as MongoValidationError, DoesNotExist
from passlib.context import CryptContext
from model import User, Project
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# MongoDB connection
try:
    connect(db="db", host=os.getenv("MONGO_URI"))
    logging.info("Connected to MongoDB Atlas successfully")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise

# Configuration variables
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM = os.getenv("ALGO", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
    role: str = None

# Utility functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_jwt(token)
    username: str = payload.get("sub")
    role: str = payload.get("role")
    if username is None or role is None:
        raise HTTPException(status_code=401, detail="Invalid token payload.")
    try:
        user = User.objects.get(username=username)
    except DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found.")
    return {"username": user.username, "role": role}

def get_current_active_user(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user.")
    return current_user

# Endpoints
@app.post("/register")
def register(username: str, password: str, role: str):
    if role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'user'.")
    if User.objects(username=username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")
    hashed_password = get_password_hash(password)
    try:
        User(username=username, password=hashed_password, role=role).save()
        return {"message": "User registered successfully."}
    except MongoValidationError as e:
        logging.error(f"Error saving user to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.objects(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/projects")
def get_projects(current_user: dict = Depends(get_current_active_user)):
    try:
        projects = Project.objects()
        return [
            {"id": project.project_id, "name": project.name, "description": project.description}
            for project in projects
        ]
    except Exception as e:
        logging.error(f"Error fetching projects: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.post("/projects")
def create_project(name: str, description: str, current_user: dict = Depends(get_current_active_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized.")
    try:
        new_project = Project(name=name, description=description)
        new_project.save()
        return {"id": new_project.project_id, "name": new_project.name, "description": new_project.description}
    except MongoValidationError as e:
        logging.error(f"Error saving project to MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.put("/projects/{project_id}")
def update_project(
    project_id: str, name: str, description: str, current_user: dict = Depends(get_current_active_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized.")
    try:
        existing_project = Project.objects.get(project_id=project_id)
        existing_project.update(name=name, description=description)
        return {"id": project_id, "name": name, "description": description}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found.")
    except MongoValidationError as e:
        logging.error(f"Error updating project in MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.delete("/projects/{project_id}")
def delete_project(project_id: str, current_user: dict = Depends(get_current_active_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized.")
    try:
        project = Project.objects.get(project_id=project_id)
        project.delete()
        return {"message": f"Project with id {project_id} has been deleted."}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found.")
    except MongoValidationError as e:
        logging.error(f"Error deleting project in MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
