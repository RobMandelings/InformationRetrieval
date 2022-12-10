import chess
import chess.pgn
from flask import request
from flask_restful import Resource

import closures
from game_indexing import retrieve


class SearchResource(Resource):

    def get(self):
        fen = request.args['state']
        str_metrics = request.args['metrics'].split(',')
        """
        Handles get requests for IR queries made by the user
        """

        board = chess.Board(fen)
        metrics = list(map(lambda str_metric: closures.Metric.from_str(str_metric), str_metrics))
        results = retrieve(board, metrics)
        return {'results': results}
