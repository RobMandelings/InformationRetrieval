import typing

import chess
import pysolr

from encoding import encoding, encoding_methods


def retrieve(solr_instance: pysolr.Solr, board: chess.Board,
             encodingMethods: typing.List[encoding_methods.EncodingMethod]):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = encoding.encode_board(board, encodingMethods)

    query = ''
    for encodingMethod, enc in board_encoding.items():
        if enc:
            if encodingMethod != encoding_methods.EncodingMethod.Check:
                query += f'{encodingMethod.field_name}:({enc}) '
            else:
                pass
                # Better if boosts are not hardcoded
                query += f'({encodingMethod.field_name}:({enc}))^{10} '

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
