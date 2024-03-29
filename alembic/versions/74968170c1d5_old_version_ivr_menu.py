"""Old version IVR menu

Revision ID: 74968170c1d5
Revises: 7b71c5a627b1
Create Date: 2018-03-17 06:43:38.959439

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "74968170c1d5"
down_revision = "7b71c5a627b1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ivrmenu")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ivrmenu",
        sa.Column("group_id", mysql.VARCHAR(length=12), nullable=False),
        sa.Column("menu_id", mysql.VARCHAR(length=12), nullable=False),
        sa.Column("menu_name", mysql.VARCHAR(length=45), nullable=True),
        sa.Column(
            "menu_current",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "menu_agentcurrent",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["advgroup.group_id"],
            name="fk_ivrmenu_group_id_advgroup",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("group_id", "menu_id"),
        mysql_default_charset="latin1",
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###
