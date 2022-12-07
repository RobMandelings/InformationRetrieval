import chess
from flask import request
from flask_restful import Resource

from game_indexing import retrieve


class SearchResource(Resource):

    def get(self):
        fen = request.args['state']
        """
        Handles get requests for IR queries made by the user
        """

        board = chess.Board(fen)
        results = retrieve(board)
        return {'results': results}
