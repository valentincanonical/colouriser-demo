#!/usr/bin/env python3
from flask import Flask, Response, abort, request
from flask_cors import CORS

from colorize import colorize_image

api = Flask(__name__)
CORS(api)

@api.route('/colorize', methods=['POST'])
def post_image(models={
    'v1': 'colorize_v1',
    'v2': 'colorize_v2'
}):
    version = request.args.get('version')
    if version not in models:
        abort(404, "This model doesn't exist")
    if 'image' not in request.files:
        abort(400, "Please send a file with key=image")
    file = request.files['image']
    return Response(colorize_image(file, models[version]), mimetype="image/jpeg")


if __name__ == '__main__':
    api.run(host="0.0.0.0")
