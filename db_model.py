from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tasks = relationship("Task", back_populates="author", cascade="all, delete-orphan")

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name


class Task(db.Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    author = relationship("User", back_populates="tasks")
