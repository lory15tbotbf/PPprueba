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
@manager.option('-n','--nombre', dest='nombre', default='nombre', help='Nombre')
@manager.option('-a','--apellido', dest='apellido', default='apellido', help='Apellido')
@manager.option('-e','--email', dest='email', default='email', help='Email')
@manager.option('-t','--telefono', dest='telefono', default='telefono', help='Telefono')
@manager.option('-o','--obs', dest='obs', default='obs', help='Obs')
def create_user(user, password, nombre, apellido, email, telefono, obs):
    from pruebita import User
    u=User(user, password, nombre, apellido, email,telefono, obs)
    db.session.add(u)
    db.session.commit()
    """Creo el usuario: user""" 

@manager.command
def dropdb():
    db.drop_all()
    """Elimino database."""

if __name__ == '__main__':
    manager.run()


