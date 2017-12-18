#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(SQLALCHEMY_DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))




db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))
