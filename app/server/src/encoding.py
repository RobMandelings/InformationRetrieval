import typing

import chess.pgn

import closures
from closures import Closure

"""
This file contains the encoding functions.

These functions are used as helper functions for the implementation of the indexing algorithm.
"""


def encode_closure(closure, closure_type: Closure):
    """
    Encodes a closure based on which closure type to the correct format

    The output of this function is added to the documents in the index
    :param closure: return value from a closure function
    :param closure_type: the type of closure to ensure right formatting
    :return: string of encoded closure
    """
    if closure_type is Closure.Reachability:
        # typing.Dict[str, float]
        closure_encodings = map(lambda pair: f"{pair[0]}{closure_type.value}{pair[1]}", list(closure.items()))
        return " ".join(closure_encodings)
    elif closure_type in {Closure.Attack, Closure.Defense}:
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
                 use_reachability: bool = True,
                 use_attack: bool = True,
                 use_defense: bool = True,
                 use_ray_attack: bool = True) -> typing.Dict[str, str]:
    """
    Encodes a board to the right format (with the given closures)

    Uses the encode_closure function
    :param board: a chess board position
    :param use_reachability: Whether to use reachability closure or not
    :param use_attack: Whether to use attack closure or not
    :param use_defense: Whether to use defense closure or not
    :param use_ray_attack: Whether to use ray attack closure or not
    :return: Full encoding of the board which is used in the indexing algorithm
    """
    base_board_list = list()
    reachability_encodings = list()
    attack_encodings = list()
    defense_encodings = list()
    ray_attack_encoding = list()

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            base_board_list.append(encode_piece_at(piece, square))

            if use_reachability:
                r_closure_enc = encode_closure(closures.reachability_closure(board, square), Closure.Reachability)
                reachability_encodings.append(r_closure_enc)
            if use_attack:
                a_closure_enc = encode_closure(closures.attack_closure(board, square), Closure.Attack)
                attack_encodings.append(a_closure_enc)
            if use_defense:
                d_closure_enc = encode_closure(closures.defense_closure(board, square), Closure.Defense)
                defense_encodings.append(d_closure_enc)
            if use_ray_attack:
                pass
                # TODO x_closure_enc = encode_closure(closures.ray_attack_closure(board, piece), Closure.RayAttack)
                # ray_attack_encoding += f"{x_closure_enc}\n"
    return {
        'board': " ".join(base_board_list),
        'reachability': " ".join(filter(lambda enc: bool(enc), reachability_encodings)),
        'attack': " ".join(filter(lambda enc: bool(enc), attack_encodings)),
        'defense': " ".join(filter(lambda enc: bool(enc), defense_encodings))
    }
