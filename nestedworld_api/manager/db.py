from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from ..app import app
from ..db import db, fixtures

migrate = Migrate(app, db)


# Management
db_manager = Manager(help='Database management commands', description='')
db_manager.add_command('migrate', MigrateCommand)


@db_manager.command
def reset():
    '''Reset the database'''

    db.drop_all()
    db.create_all()
    fixtures.reset_db()
    db.session.commit()


@db_manager.command
def import_monsters():
    fixtures.import_monsters()


@db_manager.command
def import_places():
    fixtures.import_places()
