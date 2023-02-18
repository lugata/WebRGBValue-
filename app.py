from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import cv2
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'E:/ATA/Project/Flask/Tugas 2 Kelompok 1 (PCB)/static/upload/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():

    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        pic = cv2.imread(filepath)
        picrgb = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        R = "{:.1f}".format(picrgb[:,:,0].mean())
        G = "{:.1f}".format(picrgb[:,:,1].mean())
        B = "{:.1f}".format(picrgb[:,:,2].mean())

        return render_template('index.html', filename=filename, R=R, G=G, B=B)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='upload/' + filename), code=301)
 
app.run(host="0.0.0.0",debug=True,port=2000)