# To change this template, choose Tools | Templates
# and open the template in the editor.
from flask.ext.script import Manager, Option
from pruebita import app, db

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    """Creo database"""

@manager.option('-u','--user', dest='user', default='admin', help='Username')
@manager.option('-p','--password', dest='password', default='password', help='Password')
def create_user(user, password):
    from pruebita import User
    u=User(user, password)
    db.session.add(u)
    db.session.commit()
    """Creo el usuario: user""" 

@manager.command
def dropdb():
    db.drop_all()
    """Elimino database."""

if __name__ == '__main__':
    manager.run()


