#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
import sys
from forms import *
from models import db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# TODO: connect to a local postgresql database
# Initialize the flask migrate library
db.init_app(app)
migrate = Migrate(app, db)

# DONE

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format='EEEE MMMM, d, y "at" h:mma'
  elif format == 'medium':
      format='EE MM, dd, y h:mma'
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  cities = Venue.query.distinct(Venue.city).all()
  venues = Venue.query.all()
  cityRecords=[]

  for city in cities:
    cityRecord = {
      'city': city.city,
      'state': city.state,
      'venues': [] 
    }
    for venue in venues:
      venueRecord = {
        'id': venue.id,
        'name': venue.name
      }
      if cityRecord['city'] == venue.city:
        cityRecord['venues'].append(venueRecord)
      else:
        cityx = ''      
    cityRecords.append(cityRecord)

  data = cityRecords
  # print(data)
  return render_template(
    'pages/venues.html',
    areas=data
    )

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # get the search term
  term = request.form['search_term']

  # query the database for like results and send the response
  data = Venue.query.filter(Venue.name.like('%'+term+'%')).all()
  response = {
    'count': len(data),
    'data': data
  }

  return render_template(
  'pages/search_venues.html', 
  results=response, 
  search_term=request.form.get('search_term', '')
  )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    'id': 1,
    'name': 'The Musical Hop',
    'genres': ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
    'address': '1015 Folsom Street',
    'city': 'San Francisco',
    'state': 'CA',
    'phone': '123-123-1234',
    'website': 'https://www.themusicalhop.com',
    'facebook_link': 'https://www.facebook.com/TheMusicalHop',
    'seeking_talent': True,
    'seeking_description': 'We are on the lookout for a local artist to play every two weeks. Please call us.',
    'image_link': 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    'past_shows': [{
      'artist_id': 4,
      'artist_name': 'Guns N Petals',
      'artist_image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
      'start_time': '2019-05-21T21:30:00.000Z'
    }],
    'upcoming_shows': [],
    'past_shows_count': 1,
    'upcoming_shows_count': 0,
  }
  
  data = Venue.query.filter(Venue.id==venue_id).all()
  data2 = Show.query.filter(Show.venue_id == venue_id).all()
  past_shows = []
  upcoming_shows = []

  for show in data2:
    if show.start_time < datetime.now():
      showRecord = {
        ''
      }

  result = data[0]
  data={
    'id': result.id,
    'name': result.name,
    'genres': result.genres,
    'address': result.address,
    'city': result.city,
    'state': result.state,
    'phone': result.phone,
    'website': result.phone,
    'facebook_link': result.facebook_link,
    'seeking_talent': result.seeking_talent,
    'seeking_description': result.seeking_description,
    'image_link': result.image_link,
    # 'past_shows': [{
    #   'artist_id': s.artist_id,
    #   'artist_name': s.artist_name,
    #   'artist_image_link': s.artist_image_link,
    #   'start_time': s.start_time
    # }],  
    'upcoming_shows': [],
    'past_shows_count': 1,
    'upcoming_shows_count': 0,
  }
 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  error = False
  # Declare and empty data dictionary to hold all retrieved variables
  data = {}
  try:
    # for each form data, set corresponding key in the 'data' dictionary
    data['name']=request.form['name']
    data['city']=request.form['city']
    data['state']=request.form['state']
    data['address']=request.form['address']
    data['phone']=request.form['phone']
    data['genres']=request.form['genres']
    data['facebook_link']=request.form['facebook_link']
    data['website']=request.form['website']
    if request.form['seeking_talent'] == 'Yes':
      data['seeking_talent']=True
    else:
      data['seeking_talent']=False

    data['seeking_description'] = request.form['seeking_description']
    data['image_link']=request.form['image_link']
    # set venue variable equal to corresponding model class, ready for adding to the session
    venue = Venue(
      name=data['name'], 
      city=data['city'], 
      state=data['state'], 
      address=data['address'], 
      phone=data['phone'], 
      genres=data['genres'], 
      facebook_link=data['facebook_link'],
      website=data['website'],
      seeking_talent=data['seeking_talent'],
      seeking_description=data['seeking_description'],
      image_link=data['image_link']
      )
    print(data)
    db.session.add(venue)
    # commit final changes and flash newly added venue on success
    db.session.commit()
    flash('Venue ' + data['name'] + ' was successfully listed!')
  except:
    error=True
    # if an error occurred, rollback the changes from the session and flash an error message
    db.session.rollback()
    flash('An error occurred. Venue ' + data['name'] + ' could not be listed.')
    # log error message to the console for easy debbugging
    # return(jsonify(data))
    print(sys.exc_info())
  finally:
    db.session.close()
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    'id': 4,
    'name': 'Guns N Petals',
  }, {
    'id': 5,
    'name': 'Matt Quevedo',
  }, {
    'id': 6,
    'name': 'The Wild Sax Band',
  }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for 'A' should return 'Guns N Petals', 'Matt Quevado', and 'The Wild Sax Band'.
  # search for 'band' should return 'The Wild Sax Band'.
  response={
    'count': 1,
    'data': [{
      'id': 4,
      'name': 'Guns N Petals',
      'num_upcoming_shows': 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    'id': 4,
    'name': 'Guns N Petals',
    'genres': ['Rock n Roll'],
    'city': 'San Francisco',
    'state': 'CA',
    'phone': '326-123-5000',
    'website': 'https://www.gunsnpetalsband.com',
    'facebook_link': 'https://www.facebook.com/GunsNPetals',
    'seeking_venue': True,
    'seeking_description': 'Looking for shows to perform at in the San Francisco Bay Area!',
    'image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    'past_shows': [{
      'venue_id': 1,
      'venue_name': 'The Musical Hop',
      'venue_image_link': 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
      'start_time': '2019-05-21T21:30:00.000Z'
    }],
    'upcoming_shows': [],
    'past_shows_count': 1,
    'upcoming_shows_count': 0,
  }
  data2={
    'id': 5,
    'name': 'Matt Quevedo',
    'genres': ['Jazz'],
    'city': 'New York',
    'state': 'NY',
    'phone': '300-400-5000',
    'facebook_link': 'https://www.facebook.com/mattquevedo923251523',
    'seeking_venue': False,
    'image_link': 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    'past_shows': [{
      'venue_id': 3,
      'venue_name': 'Park Square Live Music & Coffee',
      'venue_image_link': 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      'start_time': '2019-06-15T23:00:00.000Z'
    }],
    'upcoming_shows': [],
    'past_shows_count': 1,
    'upcoming_shows_count': 0,
  }
  data3={
    'id': 6,
    'name': 'The Wild Sax Band',
    'genres': ['Jazz', 'Classical'],
    'city': 'San Francisco',
    'state': 'CA',
    'phone': '432-325-5432',
    'seeking_venue': False,
    'image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'past_shows': [],
    'upcoming_shows': [{
      'venue_id': 3,
      'venue_name': 'Park Square Live Music & Coffee',
      'venue_image_link': 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      'start_time': '2035-04-01T20:00:00.000Z'
    }, {
      'venue_id': 3,
      'venue_name': 'Park Square Live Music & Coffee',
      'venue_image_link': 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      'start_time': '2035-04-08T20:00:00.000Z'
    }, {
      'venue_id': 3,
      'venue_name': 'Park Square Live Music & Coffee',
      'venue_image_link': 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
      'start_time': '2035-04-15T20:00:00.000Z'
    }],
    'past_shows_count': 0,
    'upcoming_shows_count': 3,
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    'id': 4,
    'name': 'Guns N Petals',
    'genres': ['Rock n Roll'],
    'city': 'San Francisco',
    'state': 'CA',
    'phone': '326-123-5000',
    'website': 'https://www.gunsnpetalsband.com',
    'facebook_link': 'https://www.facebook.com/GunsNPetals',
    'seeking_venue': True,
    'seeking_description': 'Looking for shows to perform at in the San Francisco Bay Area!',
    'image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    'id': 1,
    'name': 'The Musical Hop',
    'genres': ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
    'address': '1015 Folsom Street',
    'city': 'San Francisco',
    'state': 'CA',
    'phone': '123-123-1234',
    'website': 'https://www.themusicalhop.com',
    'facebook_link': 'https://www.facebook.com/TheMusicalHop',
    'seeking_talent': True,
    'seeking_description': 'We are on the lookout for a local artist to play every two weeks. Please call us.',
    'image_link': 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  # Declare and empty data dictionary to hold all retrieved variables
  data = {}
  try:
    # for each form data, set corresponding key in the 'data' dictionary
    data['name'] = request.form['name']
    data['city'] = request.form['city']
    data['state'] = request.form['state']
    data['phone'] = request.form['phone']
    data['genres'] = request.form['genres']
    data['website'] = request.form['website']
    data['facebook_link'] = request.form['facebook_link']
    if request.form['seeking_venue'] == 'Yes':
      data['seeking_venue'] = True
    else:
      data['seeking_venue'] = False
    data['seeking_description'] = request.form['seeking_description']
    data['image_link'] = request.form['image_link']
    # set artist variable equal to corresponding model class, ready for adding to the session
    artist = Artist(
      name=data['name'], 
      genres=data['genres'], 
      city=data['city'], 
      state=data['state'], 
      phone=data['phone'],
      website=data['website'],
      facebook_link=data['facebook_link'],
      seeking_venue=data['seeking_venue'],
      seeking_description=data['seeking_description'],
      image_link=data['image_link']
      )
    db.session.add(artist)
    # commit final changes and flash newly added artist on success
    db.session.commit()
    flash('Artist ' + data['name'] + ' was successfully listed!')
  except:
    error = True
    # if an error occurred, rollback the changes from the session and flash an error message
    db.session.rollback()
    flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
    # log error message to the console for easy debbugging
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    'venue_id': 1,
    'venue_name': 'The Musical Hop',
    'artist_id': 4,
    'artist_name': 'Guns N Petals',
    'artist_image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    'start_time': '2019-05-21T21:30:00.000Z'
  }, {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 5,
    'artist_name': 'Matt Quevedo',
    'artist_image_link': 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    'start_time': '2019-06-15T23:00:00.000Z'
  }, {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 6,
    'artist_name': 'The Wild Sax Band',
    'artist_image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'start_time': '2035-04-01T20:00:00.000Z'
  }, {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 6,
    'artist_name': 'The Wild Sax Band',
    'artist_image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'start_time': '2035-04-08T20:00:00.000Z'
  }, {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 6,
    'artist_name': 'The Wild Sax Band',
    'artist_image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'start_time': '2035-04-15T20:00:00.000Z'
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  # Declare and empty data dictionary to hold all retrieved variables
  data = {}
  try:
    # for each form data, set corresponding key in the 'data' dictionary
    data['artist_id'] = request.form['artist_id']
    data['venue_id'] = request.form['venue_id']
    data['start_time'] = request.form['start_time']
    # set show variable equal to corresponding model class, ready for adding to the session
    # time = Show.query.filter_by(start_time=data['start_time'])
    show = Show(
    artist_id=data['artist_id'],
    venue_id=data['venue_id'],
    start_time=data['start_time']
    )
    db.session.add(show)
    # commit final changes and flash newly added show on success
    db.session.commit()
    flash('Your show has been listed at:' + data['start_time'] + ' Thanks.')
  except:
    error = True
    # if an error occurred, rollback the changes from the session and flash an error message
    db.session.rollback()
    flash('An error occurred. Show at time:' +
          data['start_time'] + ' could not be listed.')
    # log error message to the console for easy debbugging
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
