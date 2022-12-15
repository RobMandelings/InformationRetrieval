import chess
import chess.pgn
from flask import request
from flask_restful import Resource

import solr_util
from encoding import encoding_methods
from retrieval import retrieve


class SearchResource(Resource):

    def get(self):
        fen = request.args['state']
        str_encodingMethods = request.args['encodingMethods'].split(',')
        """
        Handles get requests for IR queries made by the user
        """

        board = chess.Board(fen)
        metrics = list(map(lambda str_metric: encoding_methods.EncodingMethod.from_str(str_metric), str_encodingMethods))
        results = retrieve(solr_util.get_solr_instance(), board, metrics)
        return {'results': results}
