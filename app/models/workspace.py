from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import config
from app.deps.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    owner_id: Mapped[int] = mapped_column(
        "owner_id", ForeignKey("users.id"), nullable=False
    )
    owner = relationship("User")

    name: Mapped[str] = mapped_column("name", String(), nullable=False)

    smtp_host: Mapped[str] = mapped_column(
        "smtp_host", String(), nullable=False,
        default=config.SMTP_CONFIG_HOST
    )

    smtp_port: Mapped[int] = mapped_column(
        "smtp_port", Integer(), nullable=False,
        default=config.SMTP_CONFIG_PORT
    )

    smtp_email: Mapped[str] = mapped_column(
        "smtp_email", String(), nullable=False,
        default=config.SMTP_CONFIG_EMAIL
    )

    smtp_password: Mapped[str] = mapped_column(
        "smtp_password", String(), nullable=False,
        default=config.SMTP_CONFIG_PASSWORD
    )


class WorkspaceMembership(Base):
    __tablename__ = "memberships"

    user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id"), nullable=False
    )
    user = relationship("User", foreign_keys=[user_id], back_populates="workspaces")

    workspace_id: Mapped[int] = mapped_column(
        "workspace_id", ForeignKey("workspaces.id"), nullable=False
    )
    workspace = relationship("Workspace", foreign_keys=[workspace_id])

    role: Mapped[str] = mapped_column("role", String(), nullable=False, default="user")
