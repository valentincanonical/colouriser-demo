#!/usr/bin/env python3
from flask import Flask, json, request, send_file, Response
from flask_cors import CORS
from colorize import colorize_image

api = Flask(__name__)
CORS(api)
    
@api.route('/image', methods=['POST'])
def post_image():
  # check if the post request has the file part
  if 'image' not in request.files:
    return "Please send a file with key=image"
  file = request.files['image']
  version = request.args.get('version')
  colorized_image=colorize_image(file)
  return Response(colorized_image, mimetype="image/jpeg")

if __name__ == '__main__':
    api.run()
