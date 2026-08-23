from fastapi import FastAPI

app = FastAPI()

@app.get("/jobs")
def get_jobs():
    return {"message": "List of jobs"}

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    return {"message": f"Details of job {job_id}"}

@app.post("/login")
def login(username: str, password: str):
    return {"message": f"User {username} logged in successfully"}

@app.patch("/jobs/{job_id}")
def update_job(job_id: int, title: str | None, status: str | None):
    return {"message": f"Job {job_id} - {title} updated successfully with status: {status}"}

@app.post("/register")
def register(username: str, password: str):
    return {"message": f"User {username} registered successfully"}

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    return {"message": f"Job {job_id} deleted successfully"}