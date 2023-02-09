from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pickle
import os
import jsonpickle
import numpy as np
import requests
import urllib.request
import base64
import image_stitching
from PIL import Image
import fitz
import io 
from base64 import encodebytes
from PIL import Image
from script import script


app = Flask(__name__)
CORS(app)
# os.makedirs('temporary',exist_ok = True)
pdf_path =  "abc.pdf"

def get_response_image(image_path):
    pil_image = Image.open(image_path, mode= 'r')
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')

    return encoded_img


@app.route('/', methods=['GET', 'POST'])
def user_download():
    final_response = {'Status': 'Success'}
    if request.method == 'POST':
        # # check if the post request has the file part
        if 'uploaded_file' not in request.files:
            return jsonify({'RESPONSE', False})
        file = request.files['uploaded_file']
        if file:
            file.save('abc.pdf')
            script()
            doc = fitz.open('out.pdf')  # or fitz.Document(filename)
            total_pages = 0
            
            for page in doc:
                pix = page.get_pixmap()
                pix.save("page-%i.png" % page.number)
                total_pages+=1

            total_iter = int(total_pages/50)
            total_iter += 1

            for i in range(total_iter):
                image_stitching.stitch(i, total_pages)

            for x in range(total_pages):
                os.remove('page-%i.png'%x)

            final_response['Total_images'] = str(total_iter)
            for i in range(total_iter):
                image_path = 'final-' + str(i) + '.png'
                final_response['Image-'+ str(i)] = get_response_image(image_path)            
                os.remove(image_path)

    print(len(final_response))
    return jsonify(final_response)


if __name__ == '__main__':
    app.run(port=5000, debug=True)