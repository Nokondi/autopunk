from flask import Flask, render_template, redirect, send_file, request, flash
from magenta.models.music_vae.music_vae_generate import run
from magenta.models.music_vae.configs import CONFIG_MAP
from music21 import *
from pretty_midi import *
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from forms import *
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'eMgOaDn3sjb3S1c2s6Tt5o1KzF2MMaCt'

login = LoginManager()
login.init_app(app)

@login.user_loader
def load_user(id):
    return get_user_by_id(id)

@app.route('/')
def default_route():
    return render_template('main.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/music')
    form = LoginForm()
    if form.validate_on_submit():
        if check_user(form.username.data, form.password.data) == False:
            flash('Invalid username or password')
            return redirect('/login')
        else:
            user = get_user(form.username.data)
        login_user(user)
        return redirect('/music')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/music')
    form = RegistrationForm()
    if form.validate_on_submit():
        store_user_info(form.username.data, form.email.data, generate_password_hash(form.password.data))
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)

@app.route('/generate', methods=["POST"])
@login_required
def generate_seq():
    if(request.method=="POST"):
        create_new_song(current_user.username)
        return redirect('/music')

@app.route('/music' , methods=["GET"])
@login_required
def music():
    dir = os.listdir('./output')
    if len(dir) > 0:
        for file in dir:
            os.remove('./output/%s' % file)
    if current_user.is_authenticated:
        songs = get_songs(current_user.username)
    time_string = []
    for song in songs:
        t_pair = song.split('-')
        ts = t_pair[1].split('.')[0]
        time_string.append(datetime.utcfromtimestamp(int(ts)).strftime('%c'))
    return render_template('music.html', songs=songs, times=time_string, user=current_user.username)

@app.route('/midi_dl', methods=["POST"])
@login_required
def midi_dl():
    download_song(request.form['filename'])
    return send_file('output/%s' % request.form['filename'], as_attachment=True)

@app.route('/sheet_dl', methods=["POST"])
@login_required
def sheet_dl():
    download_song(request.form['filename'])
    song = converter.parse('output/%s' % request.form['filename'])
    for part in song.parts:
        part.removeByClass('Rest')

    return send_file(song.write('lily.pdf'), as_attachment=True)

if __name__ == '__main__':
    app.run()
