from flask import Flask,request,jsonify
from functools import wraps
# import jwt
from flask_migrate import Migrate
from models import db, information, ma, informationSchema
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:siva0304@localhost:5432/pass"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='siva'
# app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)


@app.route('/addUser',methods=['POST'])
def addUser():
    userName=request.form['user_name']
    emailId=request.form['email_id']
    password=request.form['password']
    user=information(userName,emailId,password)
    # print(user)
    db.session.add(user)
    db.session.commit()

    return f"Added --> {userName}"

@app.route('/listUsers',methods=['GET'])
def listUser():
    users=information.query.all()
    # r = [dict(row.items()) for row in users]
    # variable = {key:val for key,val in users}
    user_schema=informationSchema()
    k=[]
    for user in users:
        response=user_schema.dump(user)
        k.append(response)
    return jsonify({"users":k})


@app.route('/getUser',methods=['GET'])
def getUser():
    user=request.args.get('name')
    # print(user)
    detail=information.query.filter_by(user_name=user).first()
    user_schema=informationSchema()
    response=user_schema.dump(detail)
    return jsonify({"user":response})

@app.route('/UpdateUser', methods=['PUT','POST'])
@jwt_required()
def updateUser():
    # u=get_jwt_identity()
    # print(u)
    user=request.form['name']
    detail=information.query.filter_by(user_name=user).first()
    
    detail.email_id=request.form['new_mail_id']
    db.session.commit()

    return 'Updated!'

@app.route('/deleteUser',methods=['GET','DELETE'])
@jwt_required()
def deleteUser():
    user=request.args.get('name')
    detail=information.query.filter_by(user_name=user).first()
    db.session.delete(detail)
    db.session.commit()
    return f"Deleted"

@app.route('/login',methods=['POST'])
def login():
    if request.form['username']=='admin' and request.form['password']=='1234':
        token=create_access_token(identity={'username':request.form['username']})
        return jsonify({'token':token})
    else:
        return 'unable to verify'







if __name__ == '__main__':  
   app.run(debug = True) 
