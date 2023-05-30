from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)

    # relationship to the mission table
    missions = db.relationship("Mission", backref='planet')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ("-missions.planet",)

    def __repr__(self):
        return f'<Planet {self.id}: {self.name}>'


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)

    # relationship to the mission table
    missions = db.relationship("Mission", backref='scientist')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # serialize_only = ("id", "name", "field_of_study", "avatar")
    serialize_rules = ("-missions.scientist",)

    @validates('name')
    def validate_name(self, key, name):
        if not name and len(name) < 0:
            raise ValueError("Name must be present.")

        return name

    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study and len(field_of_study) < 0:
            raise ValueError("Name must be present.")

        return field_of_study

    def __repr__(self):
        return f'<Scientist {self.id}: {self.name}>'


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # foreign keys

    # foreing keys have plural of the model also .id
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ("-scientist.missions", "-planet.missions")

    @validates('name')
    def validate_name(self, key, name):
        if not name and len(name) < 0:
            raise ValueError("Name must be present.")

        return name

    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        if not scientist_id:
            raise ValueError("Scientist must exist")

        return scientist_id

    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        if not planet_id:
            raise ValueError("Planet must exist")

        return planet_id
