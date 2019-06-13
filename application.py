import json
import base64
import urllib.parse
import http.client
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template, url_for
import urllib.request
import os
import requests
import base64
import math
from flask import Flask
app = Flask(__name__)
#import magic

UPLOAD_FOLDER = './resources'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20000000

headers = {
    'Content-Type': 'application/octet-stream',
    'Prediction-Key': '5f57a8a9d77f4828866127c1e4fb55ff',
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/predicted')
def upload_form2():
    predictions = request.args['predictions']
    
    return render_template('upload2.html', )


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
    if file and allowed_file(file.filename):
        api_url = "https://westeurope.api.cognitive.microsoft.com/customvision/v3.0/Prediction/d618a87a-b01d-424c-a8d4-e5984af0552f/classify/iterations/test-01/image"
        
        r = requests.post(api_url, headers=headers, data=file.stream)
        parsed = r.json()
        outputs= [(x['tagName'], round(x['probability'], 3)) for x in parsed['predictions']]
        
        return render_template('upload2.html', predictions=outputs)
    else:
        flash('Allowed file types are png, jpg, jpeg')
        return redirect(request.url)
