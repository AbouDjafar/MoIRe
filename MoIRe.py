# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 12:54:12 2023

@author: Djafar

Project MoIRe : Mosaic Image Revealer
"""

import sys
from PIL import Image
import random
from flask import Flask, request, send_file, render_template

def ImageLoader(ImgURI):
    try:
        image = Image.open(ImgURI)
    except IOError:
        print('------------Erreur------------')
        sys.exit(1)
    return image

def parcoursFaisabilite(limite = 5, num = 1024, iterations = 50):
    n = 0
    i = 2
    possibles = []
    while(n < limite):
        if(num % i == 0):
            n = n + 1
            possibles.append(i)
        i = i + 1
        if(i >= iterations):
            break
    return n, possibles

"""
nombreDeBlocs() permet de connaitre combien de petits blocs d'images pouvons nous découper sur l'image principale
et grâce à parcoursFaisabilité() nous saurons les différents nombres que l'on peut utiliser pour
subdiviser l'image principale: liste_x les valeurs utilisables pour déterminer le nombre de colonnes de blocs
liste_y les valeurs possibles pour les lignes de blocs
"""
def nombreDeBlocs(img):
    colonnes, lignes = img.size
    #x le nombre de blocs selon la colonne et y selon la ligne
    x, liste_x = parcoursFaisabilite(15, colonnes, 50)
    y, liste_y = parcoursFaisabilite(15, lignes, 50)
    #print("x = ",x, "\nliste x = ", liste_x, "\ny = ", y, "\nliste y = ", liste_y)
    return x, liste_x, y, liste_y
    
def decoupageEnBlocs(img, X, Y):
    blocs = []
    colonne, ligne = img.size
    portion_x = (int)(colonne / X)
    portion_y = (int)(ligne / Y)
    k = 0
    for x in range(0, colonne, portion_x):
        k = k + 1
        l = 0
        for y in range(0, ligne, portion_y):
            l = l + 1
            #print("k = ",k, " l = ", l, "\n")
            blocs.append(((k,l),img.crop((x, y, x+portion_x, y+portion_y))))
    return blocs, (portion_x, portion_y)

def creationImage(imageDeBase, bloc, position_bloc, portions, nom):
    imageDeBase.paste(bloc, ((position_bloc[0] - 1)*portions[0], (position_bloc[1] - 1)*portions[1]))
    #print("image crée!")
    imageDeBase.save(nom)
    #print("image enregistrée!")
    return imageDeBase

import os
def creationImageEnPuzzle(image, nbr_lignes, nbr_colonnes):
    blocs, portions = decoupageEnBlocs(image, nbr_lignes, nbr_colonnes)    
    imageDeBase = Image.new('RGB', image.size)
    k = 1
    liste_ordinaire = range(0, len(blocs), 1)
    liste_desordonnee = random.sample(liste_ordinaire, len(liste_ordinaire))    
    output_directory = 'templates/output/'
    os.makedirs(output_directory, exist_ok=True)
    for i in liste_desordonnee:
        creationImage(imageDeBase, blocs[i][1], blocs[i][0], portions, "templates/output/jour {}.jpg".format(k))
        k = k+1   
    liste_images = ["templates/output/jour {}.jpg".format(i+1) for i in liste_ordinaire]
    return liste_images

import cv2
import numpy as np
def detect_faces(file):
    # Charger le fichier cascade pour la détection des visages
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Lire le fichier en tant qu'image avec OpenCV
    file_data = np.fromstring(file.read(), np.uint8)
    image = cv2.imdecode(file_data, cv2.IMREAD_UNCHANGED)
    #image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Renvoyer True s'il y a au moins un visage détecté, sinon False
    return len(faces) > 0

    
"""------------- test ----------------------------------------------------------
image = ImageLoader("jih.jpg")
creationImageEnPuzzle(image, 8, 8)  
-----------------------------------------------------------------------------"""

app = Flask(__name__, static_folder='templates')
#import logging
#logging.basicConfig(filename='MoIRe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
lignesColonnes = 0
num_img = 0

@app.route('/')
def home():
    print("hello")
    return render_template('index.html')

@app.route('/show', methods=['POST'])
def show_out():
    print("it's show out!")
    import shutil
    output_directory = 'templates/output/'
    # Vérifier si le dossier existe
    if os.path.exists(output_directory):
        # Supprimer tous les fichiers et dossiers contenus dans le dossier output
        shutil.rmtree(output_directory)
    img = ImageLoader(request.files['file'])
    #logging.info(f'Fichier reçu : {img.filename}')
    lignesColonnes = int(request.form['subdivisions'])
    #logging.info('lignesColonnes = ',lignesColonnes)
    images_puzzle = creationImageEnPuzzle(img, lignesColonnes, lignesColonnes)
    num_img = len(images_puzzle)
    #file = request.files['file']
    #if (detect_faces(file)):
    return render_template('result.html', num_images=num_img, chemins = images_puzzle)
    #else:
    #    return render_template('badThing.html')

import zipfile
import io

@app.route('/download', methods=['GET', 'POST'])
def download_all():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('templates/output/'):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    zipf.write(file_path, file)

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='PuzzleImages.zip')
    
@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)