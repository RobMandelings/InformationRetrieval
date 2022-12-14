import typing

import chess.pgn

import encoding_methods
from encoding_methods import Encoding

"""
This file contains the encoding functions.

These functions are used as helper functions for the implementation of the indexing algorithm.
"""


def encode_closure(closure, closure_type: Encoding):
    """
    Encodes a closure based on which closure type to the correct format

    The output of this function is added to the documents in the index
    :param closure: return value from a closure function
    :param closure_type: the type of closure to ensure right formatting
    :return: string of encoded closure
    """
    if closure_type is Encoding.Reachability:
        # typing.Dict[str, float]
        closure_encodings = map(lambda pair: f"{pair[0]}{closure_type.value}{pair[1]}", list(closure.items()))
        return " ".join(closure_encodings)
    elif closure_type in {Encoding.Attack, Encoding.Defense}:
        closure_encodings = []
        for (item_nr, item) in enumerate(closure[1]):
            closure_encodings.append(f"{closure[0]}{closure_type.value}{closure[1][item_nr]}")
        return " ".join(closure_encodings)


def encode_piece_at(piece, square):
    """
    TODO SEE USAGES IF THIS IS STILL USEFUL
    """
    assert piece
    assert 0 <= square <= chess.SQUARES[-1]
    return f"{piece.symbol()}{chess.square_name(square)}"


def encode_board(board: chess.Board,
                 metrics: typing.List[Encoding]) -> typing.Dict[str, str]:
    """
    Encodes a board to the right format (with the given closures)

    Uses the encode_closure function
    :param board: a chess board position
    :param metrics: optional metrics to improve the encoding of the board
    :return: Full encoding of the board which is used in the indexing algorithm
    """

    base_board_list = list()
    metric_encodings = dict()

    piece_squares = list(map(lambda square: (board.piece_at(square), square), chess.SQUARES))
    piece_squares = list(filter(lambda piece_square: bool(piece_square[0]), piece_squares))

    for (piece, square) in piece_squares:
        base_board_list.append(encode_piece_at(piece, square))

    if Encoding.Reachability in metrics:
        reachability_encodings = list()
        legal_moves_list = list(board.legal_moves)
        for (piece, square) in piece_squares:
            encoding = encode_closure(closures.reachability_closure(board, square, legal_moves_list),
                                      Encoding.Reachability)
            if encoding:
                reachability_encodings.append(encoding)
        metric_encodings[Encoding.Reachability] = " ".join(reachability_encodings)

    if Encoding.Attack in metrics:
        attack_encodings = list()
        for (piece, square) in piece_squares:
            encoding = encode_closure(closures.attack_closure(board, square), Encoding.Attack)
            if encoding:
                attack_encodings.append(encoding)
        metric_encodings[Encoding.Attack] = " ".join(attack_encodings)

    if Encoding.Defense in metrics:
        defense_encodings = list()
        for (piece, square) in piece_squares:
            encoding = encode_closure(closures.defense_closure(board, square), Encoding.Defense)
            if encoding:
                defense_encodings.append(encoding)
        metric_encodings[Encoding.Defense] = " ".join(defense_encodings)

    if Encoding.RayAttack in metrics:
        pass
        # TODO
        # ray_attack_encodings = list()
        # for square in chess.SQUARES:
        #     piece = board.piece_at(square)
        #     if piece:
        #         r_closure_enc = encode_closure(closures.ray_attack_closure(board, square), Metric.RayAttack)
        #         ray_attack_encodings.append(r_closure_enc)
        # metrics[Metric.RayAttack] = " ".join(ray_attack_encodings)

    return {
        'board': " ".join(base_board_list),
        'metrics': metric_encodings
    }
