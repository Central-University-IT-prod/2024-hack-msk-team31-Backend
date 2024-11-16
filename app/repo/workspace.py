from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.deps.database import get_session
from app.models import User
from app.models.workspace import Workspace, WorkspaceMembership


class WorkspaceRepo:
    def __init__(self, session: Session):
        self.session = session

    def find_by_user(self, user: User) -> list[Workspace]:
        return user.workspaces

    def create(self, name: str, user: User) -> Workspace:
        obj = Workspace(owner_id=user.id, name=name)
        self.session.add(obj)
        self.session.commit()
        return obj

    def find_by_id(self, uid: int) -> Workspace | None:
        stmt = select(Workspace).where(Workspace.id == uid).limit(1)
        return self.session.scalar(stmt)

    def update_name(self, uid: int, name: str) -> Workspace:
        stmt = update(Workspace).returning(Workspace).where(Workspace.id == uid)
        stmt = stmt.values(name=name)
        result = self.session.execute(stmt)
        self.session.commit()
        return result.fetchone()[0]

    def delete(self, uid: int):
        stmt = delete(Workspace).where(Workspace.id == uid)
        self.session.execute(stmt)
        self.session.commit()

    def get_users(self, uid: int) -> dict[str, str]:
        stmt = (select(WorkspaceMembership)
                .where(WorkspaceMembership.workspace_id == uid))
        users = self.session.scalars(stmt)
        return {
            user.user.login: user.role
            for user in users
        }


def get_workspace_repository(
    session: Session = Depends(get_session),
) -> Iterator[WorkspaceRepo]:
    yield WorkspaceRepo(session)


WorkspaceRepoDep = Annotated[WorkspaceRepo, Depends(get_workspace_repository)]
