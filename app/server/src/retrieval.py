import typing

import chess
import pysolr

from app.server.src.encoding import encoding, encoding_methods


def retrieve(solr_instance: pysolr.Solr, board: chess.Board, metrics: typing.List[closures.Encoding]):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = encoding.encode_board(board, metrics)

    query = f'board:({board_encoding["board"]}) '
    for metric, enc in board_encoding['metrics'].items():
        if enc:
            query += f'{metric.name.lower()}:({enc}) '

    result = solr_instance.search(
        query,
        **{
            "fl": "id,game,score,move_nr",
            "group": "true",
            "group.field": "game_id"
        })

    groups = result.grouped['game_id']['groups']
    documents = list(map(lambda group: group['doclist']['docs'][0], groups))

    # TODO improve checking
    assert groups, "no results were found"
    return documents
