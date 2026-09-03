from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from core.database import get_db
from users.models import User
from users.schemas import LoginUser, RegisterUser, UserResponse

app = FastAPI()


@app.get("/jobs")
def get_jobs():
    return {"message": "List of jobs"}


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    return {"message": f"Details of job {job_id}"}


@app.post("/login")
def login(credentials: LoginUser):
    return {"message": f"User {credentials.email} logged in successfully"}


@app.patch("/jobs/{job_id}")
def update_job(job_id: int, title: str | None, status: str | None):
    return {
        "message": f"Job {job_id} - {title} updated successfully with status: {status}"
    }


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )
    user_exists = result.scalars().first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    new_user = User(username=user.username, email=user.email, password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    return {"message": f"Job {job_id} deleted successfully"}
