from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
 
login = LoginManager()
db = SQLAlchemy()
 
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    player1 = db.Column(db.Integer)
    player2 = db.Column(db.Integer)
    player3 = db.Column(db.Integer)
    player4 = db.Column(db.Integer)
    player5 = db.Column(db.Integer)
    player6 = db.Column(db.Integer)
    player7 = db.Column(db.Integer)
    player8 = db.Column(db.Integer)
    player9 = db.Column(db.Integer)
    player10 = db.Column(db.Integer)
    player11 = db.Column(db.Integer)
    
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))