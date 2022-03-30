from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()
 
class information(db.Model):
    __tablename__ = 'details'
 
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String())
    email_id = db.Column(db.String())
    password = db.Column(db.String())
 
    def __init__(self, user_name,email_id,password):
        self.user_name = user_name
        self.email_id = email_id
        self.password = password


class informationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = information