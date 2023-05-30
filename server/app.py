from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return 'Hello world!'


class Scientists(Resource):

    def get(self):
        scientists = [s.to_dict(
            only=("id", "name", "field_of_study", "avatar")) for s in Scientist.query.all()]

        return scientists, 200

    def post(self):
        try:
            new_scientist = Scientist(
                name=request.json['name'],
                field_of_study=request.json['field_of_study'],
                avatar=request.json['avatar']
            )

            db.session.add(new_scientist)
            db.session.commit()

            return new_scientist.to_dict(only=("id", "name", "field_of_study", "avatar")), 201
        except:
            return {"error": "400: Validation error"}, 400


api.add_resource(Scientists, "/scientists")


class Planets(Resource):

    def get(self):
        try:

            planets = [p.to_dict(only=("id", "name", "distance_from_earth",
                                 "nearest_star", "image")) for p in Planet.query.all()]

            return planets, 200

        except:
            raise Exception({"error": "Something went wrong"})


api.add_resource(Planets, "/planets")


class Missions(Resource):

    def post(self):
        try:
            new_mission = Mission(
                name=request.json['name'],
                scientist_id=request.json['scientist_id'],
                planet_id=request.json['planet_id']
            )

            db.session.add(new_mission)
            db.session.commit()

            # return_mission = new_mission.
            return new_mission.planet.to_dict(only=("id", "name")), 201

        except:
            return {
                "error": "400: Validation error"
            }, 400


api.add_resource(Missions, "/missions")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
