import typing

import chess
import pysolr

from encoding import encoding, encoding_methods


def get_documents(solr_instance: pysolr.Solr, query, filter_query):
    kwargs = {
        "fl": "id,game,score,move_nr,check",
        "group": "true",
        "group.field": "game_id"
    }

    if len(filter_query) > 0:
        kwargs["fq"] = filter_query,

    result = solr_instance.search(
        query,
        **kwargs
    )

    groups = result.grouped['game_id']['groups']
    assert groups, "no results were found"
    documents = list(map(lambda group: group['doclist']['docs'][0], groups))
    return documents


def retrieve(solr_instance: pysolr.Solr, board: chess.Board,
             encodingMethods: typing.List[encoding_methods.EncodingMethod],
             filter_queries: typing.List[str]):
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

    documents = []
    if len(filter_queries) == 0:
        documents.extend(get_documents(solr_instance, query, ''))
    else:
        for filter_query in filter_queries:
            # Only top document for each filter query is kept
            documents.append(get_documents(solr_instance, query, filter_query)[0])

    return documents
