from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# Association Object
class Show (db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), primary_key=True)
    start_time = db.Column(db.DateTime)
    child=db.relationship('Artist')

    def __repr__(self):
        return f'<Show {self.id} {self.venue_id} {self.artist_id} {self.start_time}>'

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(), unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120), unique=True)
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(1000), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    children = db.relationship('Show')

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.facebook_link} {self.website} {self.seeking_talent} {self.seeking_description} {self.image_link}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(), unique=True)
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), unique=True)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(1000), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.facebook_link} {self.website} {self.seeking_venue} {self.seeking_description} {self.image_link}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # DONE

