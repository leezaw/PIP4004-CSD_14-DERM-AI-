from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import sqlite3
import pandas as pd
import numpy as np
import pickle
import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model_path1 = 'extension.h5'

CTS1 = load_model(model_path1,  compile=False)


from tensorflow.keras.preprocessing.image import load_img, img_to_array

def model_predict1(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(128,128))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
    print(result)
    #prediction = classes2[result]  
    
    if result == 0:
        return "Acne Rosacea –imples, blackheads, and  Facial redness with visible blood vessels!","result.html"        
    elif result == 1:
        return "Basal Cell Carcinoma (BCC) – A slow-growing type of skin cancer.!","result.html"
    elif result == 2:
        return "Eczema – Dry, red, itchy skin.!","result.html"
    elif result == 3:
        return "Melanoma – A serious form of skin cancer.!","result.html"
    elif result == 4:
        return "Psoriasis – Scaly patches due to immune system issues.!","result.html"
    elif result == 5:
        return "Ringworm – A fungal infection causing a circular rash.!","result.html"
    

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


@app.route('/index')
def index():
	return render_template('index.html')



@app.route('/predict2',methods=['GET','POST'])
def predict2():
    print("Entered")
    
    print("Entered here")
    file = request.files['file'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
        
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    print("@@ Predicting class......")
    pred, output_page = model_predict1(file_path,CTS1)
              
    return render_template(output_page, pred_output = pred, img_src=UPLOAD_FOLDER + file.filename)


@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    otp = random.randint(1000,5000)
    print(otp)
    msg = EmailMessage()
    msg.set_content("Your OTP is : "+str(otp))
    msg['Subject'] = 'OTP'
    msg['From'] = "myprojectstp@gmail.com"
    msg['To'] = email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("myprojectstp@gmail.com", "paxgxdrhifmqcrzn")
    s.send_message(msg)
    s.quit()
    return render_template("val.html")

@app.route("/predicts", methods=['POST'])
def predicts():
    global otp, username, name, email, number, password
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        if int(message) == otp:
            print("TRUE")
            con = sqlite3.connect('signup.db')
            cur = con.cursor()
            cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
            con.commit()
            con.close()
            return render_template("signin.html")
    return render_template("signup.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signin.html")

@app.route("/notebook")
def notebook1():
    return render_template("Notebook.html")


if __name__ == '__main__':
    app.run(debug=False)