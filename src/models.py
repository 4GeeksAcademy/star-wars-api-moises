from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites_people = db.relationship('People', secondary='favorite_people', backref='users')
    favorites_planets = db.relationship('Planet', secondary='favorite_planets', backref='users')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), primary_key=True)
