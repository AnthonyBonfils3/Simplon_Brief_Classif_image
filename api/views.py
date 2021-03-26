#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 08 12:03:47 2021

@author: Bonfils
"""

import os
import urllib.request
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pickle
from skimage.io import imread
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

width = 120
height = width

## première image pour instancier le modèle
filename = '71cfb57ce6.jpeg'
UPLOAD_FOLDER = './api/static/uploaded_imgs'## /home/anthony/Documents/Briefs/3_Block_mars_avril_deep/20210317_image_reco_CNN/api/static/uploaded_imgs ##./api/static/uploaded_imgs  

if 'uploaded_imgs' not in os.listdir('./api/static'):
    os.mkdir('./api/static/uploaded_imgs')

for file in os.listdir('./api/static/uploaded_imgs/'):
    if file != filename:
        os.remove(os.path.join(UPLOAD_FOLDER, file))


PATH = '/uploaded_imgs'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

filename_model = "api/models/Xception_21classe.h5"

model = tf.keras.models.load_model(filename_model, compile=True)
class_names = ['Bear', 'Cat', 'Chicken', 'Cow', 'Deer', 'Dog', 'Duck', 'Eagle', 'Elephant', 'Human', 'Lion', 'Monkey', 'Mouse', 'Natural', 'Panda', 'Pig', 'Pigeon', 'Rabbit', 'Sheep', 'Tiger', 'Wolf']
IMG_SIZE = 150


def predict_animal(UPLOAD_FOLDER, IMG_SIZE, model, filename):
    img = tf.keras.preprocessing.image.load_img(os.path.join(UPLOAD_FOLDER, filename), target_size=(IMG_SIZE, IMG_SIZE, 3))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    return predictions

## premiere prediction pour construire le model (pas dans le callback), pour
## que la première prédiction soit rapide
predictions = predict_animal(UPLOAD_FOLDER, IMG_SIZE, model, filename)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image = imread(os.path.join(UPLOAD_FOLDER, filename))

            predictions = predict_animal(UPLOAD_FOLDER, IMG_SIZE, model, filename)
        
            print(f"The prediction is '{class_names[np.argmax(predictions)]}' with a score of {np.max(predictions)*100:.2f}%")
            flash(class_names[np.argmax(predictions)])
            flash(round(np.max(predictions)*100,1))
            flash(os.path.join(PATH, filename))
            return redirect('/')


@app.route('/result', methods = ['POST'])
def result(im):

    #pred = model.predict(person)
    name = 'Bear'
    return render_template('result.html', name = name)

if __name__ == "__main__":
    app.run()
    

    