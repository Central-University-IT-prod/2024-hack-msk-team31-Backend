from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.deps.database import Base


class Task(Base):
    __tablename__ = "tasks"

    workspace_id: Mapped[int] = mapped_column(
        "workspace_id", ForeignKey("workspaces.id"), nullable=False
    )
    workspace = relationship("Workspace")

    author_id: Mapped[int] = mapped_column(
        "author_id", ForeignKey("users.id"), nullable=False
    )
    author = relationship("User")

    name: Mapped[str] = mapped_column("name", String(), nullable=False)
    # tag1;tag2;tag3
    tags: Mapped[str] = mapped_column("tags", String(), nullable=False)
    deadline: Mapped[datetime] = mapped_column("deadline", DateTime(), nullable=True)
    content: Mapped[str] = mapped_column("content", String(), nullable=False)
    description: Mapped[str] = mapped_column("description", String(), nullable=False)

    checks: Mapped[dict] = mapped_column("checks", JSON(), nullable=False)


class TaskUpdateEvent(Base):
    __tablename__ = "task_update_events"

    task_id: Mapped[int] = mapped_column(
        "task_id", ForeignKey("tasks.id"), nullable=False
    )
    task = relationship("Task")

    author_id: Mapped[int] = mapped_column(
        "author_id", ForeignKey("users.id"), nullable=False
    )
    author = relationship("User")
