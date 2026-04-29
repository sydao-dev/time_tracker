from fastapi import FastAPI

from .api.endpoints import users, auth
from .db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Time Tracker API",
    description="Backend API for the Time Tracker Desktop App",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Time Tracker API! Server is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}