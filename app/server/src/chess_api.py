from flask import request
from flask_restful import Resource


class SearchResource(Resource):

    def get(self):
        state = request.args['state']
        """
        Handles get requests for IR queries made by the user
        """
        # result = parse.unquote(state_encoding)
        return {'msg': state}
        pass
