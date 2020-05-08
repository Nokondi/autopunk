from flask import Flask, render_template, redirect, send_file, request, flash
from magenta.models.music_vae.music_vae_generate import run, FLAGS
from magenta.models.music_vae.configs import CONFIG_MAP
from mingus.midi import midi_file_in
import mingus.extra.lilypond as LilyPond
from music21 import *
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from forms import *

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
        args = {
            "config":"hierdec-trio_16bar",
            "checkpoint_file":"./checkpoints/train1000.tar",
            "mode":"sample",
            "num_outputs":1,
            "output_dir":"./output"
        }
        filename = run(CONFIG_MAP, args)
        add_song(current_user.username, filename)
        return redirect('/music')

@app.route('/music' , methods=["GET"])
@login_required
def music():
    if current_user.is_authenticated:
        songs = get_songs(current_user.username)
    return render_template('music.html', songs=songs)

@app.route('/midi_dl', methods=["POST"])
@login_required
def midi_dl():
    return send_file(request.form['filename'], as_attachment=True)

@app.route('/sheet_dl', methods=["POST"])
@login_required
def sheet_dl():
    print(request.form['filename'])
    song = converter.parse(request.form['filename'])
    sheet = song.write('lily.pdf')
    print(sheet)
    #return send_file(l, as_attachment=True)
    return send_file(sheet, as_attachment=True)

if __name__ == '__main__':
    app.run()
