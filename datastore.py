from google.cloud import datastore
ds_client = datastore.Client()

def store_user_info(user):
    new_user = datastore.Entity(ds_client.key('user', user['email']))
    new_user.update({
        'f_name': user['f_name'],
        'l_name': user['l_name'],
        'pw': user['pw_hash'],
        'songs': []
    })
    ds_client.put(new_user)

def add_song(email, song):
    user = ds_client.get(ds_client.key('user', email))
    user['songs'].append(song)
    ds_client.put(user)

def get_songs(email):
    user = ds_client.get(ds_client.key('user', email))
    return user['songs']