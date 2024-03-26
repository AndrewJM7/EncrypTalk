from app import db, app
import bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    
    def __init__(self, email, firstname, lastname, password):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        # hashing password and using salt for more protection
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
    def is_active(self):
        return True
    
    def get_id(self):
        return (self.id)


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
