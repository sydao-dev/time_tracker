from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Table, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

time_entry_tags = Table(
    "time_entry_tags",
    Base.metadata,
    Column("time_entry_id", Integer, ForeignKey("time_entries.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    time_entries = relationship("TimeEntry", back_populates="owner", cascade="all, delete-orphan")

    clients = relationship("Client", back_populates="owner", cascade="all, delete-orphan")

    tags = relationship("Tag", back_populates="owner", cascade="all, delete-orphan")

    pomodoro_focus = Column(Integer, default=25)
    pomodoro_short_break = Column(Integer, default=5)
    pomodoro_long_break = Column(Integer, default=15)

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    time_entries = relationship("TimeEntry", back_populates="owner", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="owner", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="owner", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#000000")
    hourly_rate = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    is_archived = Column(Boolean, default=False)

    owner = relationship("User", back_populates="projects")
    time_entries = relationship("TimeEntry", back_populates="project")
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    client = relationship("Client", back_populates="projects")

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, default="No description")
    start_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)

    is_archived = Column(Boolean, default=False)

    owner = relationship("User", back_populates="time_entries")
    project = relationship("Project", back_populates="time_entries")

    tags = relationship("Tag", secondary=time_entry_tags, back_populates="time_entries")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="clients")
    projects = relationship("Project", back_populates="client")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#808080")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tags")
    time_entries = relationship("TimeEntry", secondary=time_entry_tags, back_populates="tags")