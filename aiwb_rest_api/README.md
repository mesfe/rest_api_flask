DataNet and ModelNet Predix Microservices
=========
Schema design, migration, database versioning, and REST API for DataNet and ModelNet microservices as a part of deployement of AIWB to the platform. See the confluence page
[here](https://devcloud.swcoe.ge.com/devspace/pages/viewpage.action?pageId=1206595873).

Installation
------------

Create a virtual envoironment.
Install the dependencies with `pip install -r requirements.txt`<br />
Create the database with `db_create.py` script.<br />
Check-in your database updates to the db_repository folder with `db_migrate.py`<br />
Push your updates to database with `db_upgrade.py`<br />
( You can rollback your database to the last version with `db_downgrade.py`)<br />



Running
-------
Run the app with `run.py` script from your virtual env.
