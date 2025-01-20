import os
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Resource, Api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

###################################################
################ CONFIGURATIONS ###################
##################################################

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
jwt = JWTManager(app)

api = Api(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

###################################################
################ MODELS ###########################
##################################################


class Puppy(db.Model):
    name = db.Column(db.String(80),primary_key=True)


    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name': self.name}

    def __str__(self):
        return f"{self.name} "

###################################################
################ RESOURCES ###########################
##################################################

class PuppyNames(Resource):
    def get(self,name):

        pup = Puppy.query.filter_by(name=name).first()

        if pup:
            return pup.json()
        else:
            # If you request a puppy not yet in the puppies list
            return {'name':'not found'}, 404

    def post(self, name):
        
        pup = Puppy(name=name)
        db.session.add(pup)
        db.session.commit()

        return pup.json()

    def delete(self,name):

        pup = Puppy.query.filter_by(name=name).first()
        db.session.delete(pup)
        db.session.commit()

        return {'note':'delete successful'}




class AllNames(Resource):

    @jwt_required()
    def get(self):
        # return all the puppies :)
        puppies = Puppy.query.all()

        # return json of (puppies)
        return [pup.json() for pup in puppies]


api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames,'/puppies')

if __name__ == "__main__":
    app.run(debug=True)