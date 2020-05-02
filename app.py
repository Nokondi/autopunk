from flask import Flask, render_template, redirect, send_file, request
from magenta.models.music_vae.music_vae_generate import run, FLAGS
from magenta.models.music_vae.configs import CONFIG_MAP
from music21 import *
from flask_login import LoginManager
from datastore import *

app = Flask(__name__)

login = LoginManager(app)

@app.route('/')
def default_route():
    return render_template('main.html')

@app.route('/generate', methods=["POST"])
def generate_seq():
    if(request.method=="POST"):
        args = {
            "config":"hierdec-trio_16bar",
            "checkpoint_file":"./checkpoints/train1000.tar",
            "mode":"sample",
            "num_outputs":1,
            "output_dir":"%s/output" % app.root_path
        }
        ts = run(CONFIG_MAP, args)
        return redirect('/music')

@app.route('/music' , methods=["GET"])
def music():
    return render_template('music.html')

@app.route('/midi_dl', methods=["POST"])
def midi_dl():
    filestring = "hierdec-trio_16bar_sample_%s-000-of-001.mid" % ts
    send_file("output/%s" % filestring, as_attachment=True)
    return redirect('/music')

@app.route('/sheet_dl', methods=["POST"])
def sheet_dl():
    midi.translate.midiFilePathToStream()
    return redirect('/music')

if __name__ == '__main__':
    app.run()
