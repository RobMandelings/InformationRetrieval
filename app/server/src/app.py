from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api

import chess_api

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pongewong!')


api.add_resource(chess_api.SearchResource, '/api/search')

if __name__ == '__main__':
    app.run()
