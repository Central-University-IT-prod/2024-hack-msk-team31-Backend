"""new stages system

Revision ID: 1408672a0ca5
Revises: 0be17b4c4021
Create Date: 2024-11-09 12:24:21.358440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1408672a0ca5"
down_revision: Union[str, None] = "0be17b4c4021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "task_update_events",
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("workflow_events")
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.drop_column("tasks", "stage_id")
    op.drop_table("stages")
    op.add_column("tasks", sa.Column("checks", sa.JSON(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "stages",
        sa.Column("workspace_id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("color", sa.VARCHAR(), nullable=False),
        sa.Column("indicates_ready", sa.BOOLEAN(), nullable=False),
        sa.Column("next_stage_id", sa.INTEGER(), nullable=True),
        sa.Column("stage_id", sa.INTEGER(), nullable=True),
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created_at",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["next_stage_id"],
            ["stages.id"],
        ),
        sa.ForeignKeyConstraint(
            ["stage_id"],
            ["stages.id"],
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("tasks", sa.Column("stage_id", sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, "tasks", "stages", ["stage_id"], ["id"])
    op.drop_column("tasks", "checks")
    op.create_table(
        "workflow_events",
        sa.Column("next_stage_id", sa.INTEGER(), nullable=True),
        sa.Column("stage_id", sa.INTEGER(), nullable=True),
        sa.Column("user_id", sa.INTEGER(), nullable=False),
        sa.Column("event_time", sa.DATETIME(), nullable=False),
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column(
            "created_at",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["next_stage_id"],
            ["stages.id"],
        ),
        sa.ForeignKeyConstraint(
            ["stage_id"],
            ["stages.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("task_update_events")
    # ### end Alembic commands ###
