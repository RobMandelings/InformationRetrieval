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
                 use_ray_attack: bool = True) -> str:
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
    closure_encodings = ""
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            base_board_list.append(encode_piece_at(piece, square))

            if use_reachability:
                r_closure_enc = closures.reachability_closure(board, square)
                closure_encodings += f"{r_closure_enc}\n"
            if use_attack:
                a_closure_enc = closures.attack_closure(board, square)
                closure_encodings += f"{a_closure_enc}\n"
            if use_defense:
                d_closure_enc = closures.defense_closure(board, square)
                closure_encodings += f"{d_closure_enc}\n"
            if use_ray_attack:
                x_closure_enc = closures.ray_attack_closure(board, piece)
                closure_encodings += f"{x_closure_enc}\n"

    base_board_encoding = " ".join(base_board_list)
    return f"{base_board_encoding}\n{closure_encodings}"
