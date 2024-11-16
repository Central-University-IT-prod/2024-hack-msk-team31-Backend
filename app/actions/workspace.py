from app.deps.email_sender import Message, AbstractSender, SMTPConfig, EmailSender
from app.repo.workspace import WorkspaceRepo


def notify_roles_in_workspace(
        workspace_repo: WorkspaceRepo,
        workspace_id: int,
        roles: list[str],
        message: Message
):
    members = [
        user.email
        for user, role in workspace_repo.get_users(workspace_id).items()
        if role in roles
    ]
    mass_send(
        members,
        EmailSender(get_workspace_email_config(
            workspace_repo, workspace_id
        )),
        message
    )


def get_workspace_email_config(
        workspace_repo: WorkspaceRepo,
        workspace_id: int
):
    ws = workspace_repo.find_by_id(workspace_id)
    return SMTPConfig(
        host=ws.smtp_host,
        port=ws.smtp_port,
        email=ws.smtp_email,
        password=ws.smtp_password
    )


def mass_send(addresses: list[str], sender: AbstractSender, message: Message):
    for address in addresses:
        sender.send(address, message)
