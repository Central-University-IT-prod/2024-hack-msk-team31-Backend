from fastapi import APIRouter

from app.asserts import assert401, assert404
from app.deps.tokens import UserDep
from app.repo.workspace import WorkspaceRepoDep
from app.schemas.workspace import (
    WorkspaceCreateModel,
    WorkspaceResponseModel,
    WorkspaceUpdateModel,
)

router = APIRouter(tags=["Workspace"])


@router.post(
    "/workspaces",
    response_model=WorkspaceResponseModel,
    description="Create a new workspace",
    responses={
        200: {"description": "Workspace created successfully"},
        401: {"description": "Authentication failed"},
    },
)
def create_workspace(
    data: WorkspaceCreateModel,
    user: UserDep,
    repo: WorkspaceRepoDep,
):
    workspace = repo.create(name=data.name, user=user)
    return workspace


@router.get(
    "/workspaces",
    response_model=list[WorkspaceResponseModel],
    description="List all workspaces owned by the authenticated user",
    responses={
        200: {"description": "List of workspaces returned successfully"},
        401: {"description": "Authentication failed"},
    },
)
def list_workspaces(
    user: UserDep,
    repo: WorkspaceRepoDep,
):
    return repo.find_by_user(user)


@router.get(
    "/workspaces/{workspace_id}",
    response_model=WorkspaceResponseModel,
    description="Get workspace by ID",
    responses={
        200: {"description": "Workspace returned successfully"},
        401: {"description": "Not authorized to access this workspace"},
        404: {"description": "Workspace not found"},
    },
)
def get_workspace(
    workspace_id: int,
    user: UserDep,
    repo: WorkspaceRepoDep,
):
    workspace = repo.find_by_id(workspace_id)
    assert404(workspace)
    assert401(workspace.owner_id == user.id)
    return workspace


@router.put(
    "/workspaces/{workspace_id}",
    response_model=WorkspaceResponseModel,
    description="Update workspace name",
    responses={
        200: {"description": "Workspace updated successfully"},
        401: {"description": "Not authorized to modify this workspace"},
        404: {"description": "Workspace not found"},
    },
)
def update_workspace(
    workspace_id: int,
    data: WorkspaceUpdateModel,
    user: UserDep,
    repo: WorkspaceRepoDep,
):
    workspace = repo.find_by_id(workspace_id)
    assert404(workspace)
    assert401(workspace.owner_id == user.id)
    return repo.update_name(workspace_id, data.name)


@router.delete(
    "/workspaces/{workspace_id}",
    description="Delete workspace",
    responses={
        204: {"description": "Workspace was deleted."},
        401: {"description": "Not authorized to delete this workspace"},
        404: {"description": "Workspace not found"},
    },
)
def delete_workspace(
    workspace_id: int,
    user: UserDep,
    repo: WorkspaceRepoDep,
):
    workspace = repo.find_by_id(workspace_id)
    assert404(workspace)
    assert401(workspace.owner_id == user.id)
    repo.delete(workspace_id)
