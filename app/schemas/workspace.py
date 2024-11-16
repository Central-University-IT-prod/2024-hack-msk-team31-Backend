from app.schemas import BaseSchema


class WorkspaceBaseModel(BaseSchema):
    name: str


class WorkspaceCreateModel(WorkspaceBaseModel):
    pass


class WorkspaceUpdateModel(WorkspaceBaseModel):
    pass


class WorkspaceResponseModel(WorkspaceBaseModel):
    id: int
    owner_id: int
