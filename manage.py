from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db, Movie, Actor

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# seed data prepared for database loading
@manager.command
def seed():
    Movie(title='Wonder Woman 1984', release_date='2020-12-16').insert()
    Movie(title='Space Sweepers', release_date='2021-02-05').insert()
    Movie(title='Star Wars: The Rise of Skywalker (Episode IX)', release_date='2019-12-19').insert()
    Movie(title='The Matrix Reloaded', release_date='2003-05-15').insert()
    Movie(title='Parasite', release_date='2019-05-21').insert()

    Actor(name='Tom Cruise', gender='male', age=58).insert()
    Actor(name='Angelina Jolie', gender='female', age=45).insert()
    Actor(name='Tom Hanks', gender='male', age=64).insert()
    Actor(name='Meryl Streep', gender='female', age=71).insert()
    Actor(name='Nicole Kidman', gender='female', age=53).insert()


if __name__ == '__main__':
    manager.run()
