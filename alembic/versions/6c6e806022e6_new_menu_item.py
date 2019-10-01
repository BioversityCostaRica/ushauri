"""New Menu item

Revision ID: 6c6e806022e6
Revises: f10491ed9419
Create Date: 2018-03-17 07:03:31.362644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6c6e806022e6"
down_revision = "f10491ed9419"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "menuitem",
        sa.Column("item_id", sa.String(length=12), nullable=False),
        sa.Column("item_type", sa.Integer(), nullable=True),
        sa.Column("item_desc", sa.Text(), nullable=True),
        sa.Column("item_pos", sa.Integer(), nullable=True),
        sa.Column("next_item", sa.String(length=12), nullable=True),
        sa.Column("menu_id", sa.String(length=12), nullable=False),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["ivrmenu.menu_id"],
            name=op.f("fk_menuitem_menu_id_ivrmenu"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["next_item"],
            ["menuitem.item_id"],
            name=op.f("fk_menuitem_next_item_menuitem"),
        ),
        sa.PrimaryKeyConstraint("item_id", name=op.f("pk_menuitem")),
    )
    op.create_index(op.f("ix_menuitem_menu_id"), "menuitem", ["menu_id"], unique=False)
    op.create_index(
        op.f("ix_menuitem_next_item"), "menuitem", ["next_item"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_menuitem_next_item"), table_name="menuitem")
    op.drop_index(op.f("ix_menuitem_menu_id"), table_name="menuitem")
    op.drop_table("menuitem")
    # ### end Alembic commands ###
