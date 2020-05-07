from flask_login import UserMixin
from google.cloud import datastore, ndb
from werkzeug.security import generate_password_hash, check_password_hash

ds_client = datastore.Client()
ndb_client = ndb.Client()

class User(UserMixin, ndb.Model):
    id = ndb.IntegerProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    password_hash = ndb.StringProperty()

def get_user(username):
    with ndb_client.context():
        query = User.query(User.username == username)
        current_user = None
        for u in query:
            current_user = User(id=u.key.id(), username=u.username, email=u.email, password_hash=u.password_hash)
        return current_user

def get_user_by_id(id):
    with ndb_client.context():
        key = ndb.Key(User, int(id))
        u = key.get()
        return User(id=u.key.id(), username=u.username, email=u.email, password_hash=u.password_hash)

def store_user_info(username, email, password_hash):
    with ndb_client.context():
        new_user = User(username=username, email=email, password_hash=password_hash)
        new_user.put()

def check_user(username, password):
    with ndb_client.context():
        query = User.query(User.username == username)
        for u in query:
            result = check_password_hash(u.password_hash, password)
        return result


class Song(ndb.Model):
    user = ndb.StringProperty()
    filename = ndb.StringProperty()

def add_song(username, song):
    with ndb_client.context():
        new_song = Song(user=username, filename=song)
        new_song.put()

def get_songs(username):
    with ndb_client.context():
        query = Song.query().filter(Song.user == username)
        songs = []
        for s in query:
            songs.append(str(s.filename))
        return songs