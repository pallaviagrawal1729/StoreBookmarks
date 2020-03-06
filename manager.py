from bookmarkProject import db, app
from flask_script import Manager, prompt_bool
from bookmarkProject.model import User

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="pallavi",email="wacky.pallavi@gmail.com", password="test"))
    db.session.add(User(username="priyanka", email="pg21gupta@gmail.com", password="test"))
    db.session.commit()
    print('Initialized db')


@manager.command
def dropdb():
    if prompt_bool('are you sure you want to lose all your data'):
        db.drop_all()
        print("dropped database")


if __name__ == '__main__':
    manager.run()
