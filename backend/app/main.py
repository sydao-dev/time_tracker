from fastapi import FastAPI

from .api.endpoints import users, auth, projects, time_entries, reports, clients, tags
from .db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Time Tracker API",
    description="Backend API for the Time Tracker Desktop App",
    version="1.0.0"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(time_entries.router, prefix="/time-entries", tags=["Time Entries"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Time Tracker API! Server is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}