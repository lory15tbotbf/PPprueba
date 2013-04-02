# To change this template, choose Tools | Templates
# and open the template in the editor.
from flask.ext.script import Manager, Option
from pruebita import app, db

manager = Manager(app)

@manager.command
def initdb():
    print """Creates all database tables."""
    db.create_all()

@manager.option('-u','--user', dest='user', default='admin', help='Username')
@manager.option('-p','--password', dest='password', default='password', help='Password')
def create_user(user, password):
    print """Creates the admin user."""
    from pruebita import User
    u=User(user, password)
    db.session.add(u)
    db.session.commit()

@manager.command
def dropdb():
    print """Drops all database tables."""
    db.drop_all()

if __name__ == '__main__':
    manager.run()


