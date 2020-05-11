import time
from flask_login import UserMixin
from google.cloud import datastore, ndb, storage
from werkzeug.security import generate_password_hash, check_password_hash
from magenta.models.music_vae.music_vae_generate import run
from magenta.models.music_vae.configs import CONFIG_MAP
from music21 import *
from pretty_midi import *
import os

ds_client = datastore.Client()
ndb_client = ndb.Client()
storage_client = storage.Client()

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
        key = ndb.Key('User', int(id))
        u = key.get()
        if u:
            return User(id=u.key.id(), username=u.username, email=u.email, password_hash=u.password_hash)
        else:
            return None

def store_user_info(username, email, password_hash):
    with ndb_client.context():
        new_user = User(username=username, email=email, password_hash=password_hash)
        new_user.put()

def check_user(username, password):
    with ndb_client.context():
        query = User.query(User.username == username)
        result = False
        for u in query:
            result = check_password_hash(u.password_hash, password)
        return result


class Song(ndb.Model):
    user = ndb.StringProperty()
    filename = ndb.StringProperty()

def create_new_song(username):

    # Generate song
    args = {
        "config": "hierdec-trio_16bar",
        "checkpoint_file": "./checkpoints/train1000.tar",
        "mode": "sample",
        "num_outputs": 1,
        "output_dir": "./output"
    }
    song_file = run(CONFIG_MAP, args)

    # Modify contents of midi file
    midi_data = PrettyMIDI(song_file)
    for instrument in midi_data.instruments:
        if instrument.program == 0 and instrument.is_drum == False:
            instrument.program = 29
    midi_data.write(song_file)

    # Upload song to cloud bucket and data to ndb
    ts = time.time()
    song_name = '%s-%s.mid' % (username, ts)
    bucket = storage_client.bucket('autopunk-data')
    blob = bucket.blob(song_name)
    blob.upload_from_filename(song_file)
    with ndb_client.context():
        new_song = Song(user=username, filename=song_name)
        new_song.put()

    # Delete file from local storage
    os.remove(song_file)

def get_songs(username):
    with ndb_client.context():
        query = Song.query().filter(Song.user == username)
        songs = []
        for s in query:
            songs.append(str(s.filename))
        songs.reverse()
        return songs

def download_song(song):
    bucket = storage_client.get_bucket('autopunk-data')
    blob = storage.Blob(song, bucket)
    with open('output/%s' % song, 'wb') as file_obj:
        storage_client.download_blob_to_file(blob, file_obj)
