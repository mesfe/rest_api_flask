from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
todo = Table('todo', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('text', VARCHAR(length=50)),
    Column('complete', BOOLEAN),
    Column('user_id', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('public_id', VARCHAR(length=50)),
    Column('name', VARCHAR(length=50)),
    Column('password', VARCHAR(length=80)),
    Column('admin', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['todo'].drop()
    pre_meta.tables['user'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['todo'].create()
    pre_meta.tables['user'].create()
