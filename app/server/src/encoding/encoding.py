import typing

import chess.pgn
import encoding.encoding_methods as encoding_methods

"""
This file contains the encoding functions.

These functions are used as helper functions for the implementation of the indexing algorithm.
"""


def encode_closure(closure, closure_type: encoding_methods.EncodingMethod):
    """
    Encodes a closure based on which closure type to the correct format

    The output of this function is added to the documents in the index
    :param closure: return value from a closure function
    :param closure_type: the type of closure to ensure right formatting
    :return: string of encoded closure
    """
    if closure_type is encoding_methods.EncodingMethod.Reachability:
        # typing.Dict[str, float]
        closure_encodings = map(lambda pair: f"{pair[0]}{closure_type.value}{pair[1]}", list(closure.items()))
        return " ".join(closure_encodings)
    elif closure_type in {encoding_methods.EncodingMethod.Attack, encoding_methods.EncodingMethod.Defense,
                          encoding_methods.EncodingMethod.RayAttack}:
        closure_encodings = []
        for (item_nr, item) in enumerate(closure[1]):
            closure_encodings.append(f"{closure[0]}{closure_type.value}{closure[1][item_nr]}")
        return " ".join(closure_encodings)
    elif closure_type is encoding_methods.EncodingMethod.Check:
        closure_encoding = None
        if closure[0]:
            closure_encoding = closure[1]
        return closure_encoding


def encode_board(board: chess.Board,
                 metrics: typing.List[encoding_methods.EncodingMethod]) -> typing.Dict[encoding_methods.EncodingMethod, str]:
    """
    Encodes a board to the right format (with the given closures)

    Uses the encode_closure function
    :param board: a chess board position
    :param metrics: optional metrics to improve the encoding of the board
    :return: Full encoding of the board which is used in the indexing algorithm
    """

    board_encoding = {}
    base_board_list = list()

    piece_squares = list(map(lambda square: (board.piece_at(square), square), chess.SQUARES))
    piece_squares = list(filter(lambda piece_square: bool(piece_square[0]), piece_squares))

    for (piece, square) in piece_squares:
        base_board_list.append(encoding_methods.encode_piece_at(piece, square))

    if encoding_methods.EncodingMethod.Reachability in metrics:
        reachability_encodings = list()
        legal_moves_list = list(board.legal_moves)
        for (piece, square) in piece_squares:
            encoding = encode_closure(encoding_methods.reachability_closure(board, square, legal_moves_list),
                                      encoding_methods.EncodingMethod.Reachability)
            if encoding:
                reachability_encodings.append(encoding)
        board_encoding[encoding_methods.EncodingMethod.Reachability] = " ".join(reachability_encodings)

    if encoding_methods.EncodingMethod.Attack in metrics:
        attack_encodings = list()
        for (piece, square) in piece_squares:
            encoding = encode_closure(encoding_methods.attack_closure(board, square), encoding_methods.EncodingMethod.Attack)
            if encoding:
                attack_encodings.append(encoding)
        board_encoding[encoding_methods.EncodingMethod.Attack] = " ".join(attack_encodings)

    if encoding_methods.EncodingMethod.Defense in metrics:
        defense_encodings = list()
        for (piece, square) in piece_squares:
            encoding = encode_closure(encoding_methods.defense_closure(board, square),
                                      encoding_methods.EncodingMethod.Defense)
            if encoding:
                defense_encodings.append(encoding)
        board_encoding[encoding_methods.EncodingMethod.Defense] = " ".join(defense_encodings)

    if encoding_methods.EncodingMethod.RayAttack in metrics:
        ray_attack_encodings = list()
        for (piece, square) in piece_squares:
            encoding = encode_closure(encoding_methods.ray_attack_closure(board, square),
                                      encoding_methods.EncodingMethod.RayAttack)
            if encoding:
                ray_attack_encodings.append(encoding)
        board_encoding[encoding_methods.EncodingMethod.RayAttack] = " ".join(ray_attack_encodings)

    if encoding_methods.EncodingMethod.Check in metrics:
        check_encodings = list()
        for (piece, square) in piece_squares:
            encoding = encode_closure(encoding_methods.check(board, square), encoding_methods.EncodingMethod.Check)
            if encoding:
                check_encodings.append(encoding)
        board_encoding[encoding_methods.EncodingMethod.Check] = " ".join(check_encodings)

    board_encoding[encoding_methods.EncodingMethod.Board] = " ".join(base_board_list)
    return board_encoding
