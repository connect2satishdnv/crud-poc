# --- File: api/main.py ---
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List
import jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()

# DB
users_db = {"admin": {"username": "admin", "hashed_password": pwd_context.hash("admin")}}
tasks = []

class Task(BaseModel):
    id: int
    title: str

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user['username'], "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tasks", response_model=List[Task])
def get_tasks(token: dict = Depends(verify_token)):
    return tasks

@app.post("/tasks")
def create_task(task: Task, token: dict = Depends(verify_token)):
    tasks.append(task)
    return {"message": "Task created"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, token: dict = Depends(verify_token)):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Task deleted"}
