import os
import random
from keys import *
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, abort
import json
import numpy as np
import boto3
# from flask_mobility import Mobility
# from flask_mobility.decorators import mobile_template

# from PIL import Image
# from io import BytesIO
# import base64
# import cv2

app = Flask(__name__)

percentiles = np.arange(1, 101)

@app.route('/')
def index():
  rom = random.choice(['qbert', 'spaceinvaders', 'mspacman', 'pinball', 'revenge']) 
  return render_template('index.html', rom=rom, ai_score=0)

@app.route('/<rom>')
def index_rom(rom):
  if(rom not in ['qbert', 'spaceinvaders', 'mspacman', 'pinball', 'revenge']):
    return redirect('/')
  return render_template('index.html', rom=rom, ai_score=0)

@app.route("/blank")
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
  print(store)

  return "finished"

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/data')
def data():
  return render_template('data.html')

if __name__ == "__main__":
  app.run()