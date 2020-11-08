import os
import random
from keys import *
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, abort, session
import json
import numpy as np
import boto3
import string
from flask_session import Session
# from flask_mobility import Mobility
# from flask_mobility.decorators import mobile_template

# from PIL import Image
# from io import BytesIO
# import base64
# import cv2

app = Flask(__name__)
app.secret_key = 'afisdosad90akfsdial1239jk'
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)



@app.route('/')
def instruct():
  return render_template('instruct.html')

# both do the same thing. functionally the same, but I needed another for a href call in JS
@app.route('/start')
def start():
  return render_template('instruct.html')

@app.route('/trial')
def trial():
  rom = 'spaceinvaders'
  return render_template('trial.html', rom=rom, ai_score=0)

@app.route('/after_trial')
def after_trial():
  return render_template('instruct2.html')

@app.route('/game')
def game():
  rom = 'spaceinvaders'
  return render_template('index.html', rom=rom, ai_score=0)




def ran_gen(size, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for x in range(size))

@app.route('/key')
def key():
  # rom = random.choice(['qbert', 'spaceinvaders', 'mspacman', 'pinball', 'revenge'])
  return jsonify({"key": ran_gen(10, "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")})

# @app.route('/<rom>')
# def index_rom(rom):
#   if(rom not in ['qbert', 'spaceinvaders', 'mspacman', 'pinball', 'revenge']):
#     return redirect('/')
#   return render_template('index.html', rom=rom, ai_score=0)

@app.route("/mic")
def blank():
  return render_template('blank.html')

@app.route('/sign_s3/')
def sign_s3():
    #   S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_BUCKET = 'atari11'
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3', region_name='us-east-2', config = boto3.session.Config(signature_version='s3v4'))

    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name),
        'key': file_name
    })

@app.route("/api/save", methods=["POST"])
def api_save():
  # save information on S3
  store = request.get_json()
  return "finished"

if __name__ == "__main__":
  app.run()