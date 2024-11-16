from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.deps.database import Base


class Comment(Base):
    __tablename__ = "comments"

    task_id: Mapped[int] = mapped_column(
        "task_id", ForeignKey("tasks.id"), nullable=False
    )
    task = relationship("Task")

    text: Mapped[str] = mapped_column("text", String(), nullable=False)

    user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id"), nullable=False
    )
    user = relationship("User")

    post_time: Mapped[datetime] = mapped_column("post_time", DateTime(), nullable=False)
