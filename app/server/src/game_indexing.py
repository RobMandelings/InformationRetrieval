import enum
import typing

import chess.pgn


class Closure(enum.Enum):
    Reachability = '|'
    Attack = '>'
    Defense = '<'
    RayAttack = '='


def encode_closure(closure: typing.Dict[str, float], closure_type: Closure):
    closure_encodings = map(lambda pair: f"{pair[0]}{closure_type.value}{pair[1]}", list(closure.items()))
    return " ".join(closure_encodings)


def reachability_closure(board: chess.Board, piece: chess.Piece) -> typing.Dict[str, float]:
    """
    Computes the reachability closure of a piece on the given board
    """
    pass


def attack_closure(board: chess.Board, piece: chess.Piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass


def defense_closure(board: chess.Board, piece: chess.Piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass


def ray_attack_closure(board: chess.Board, piece: chess.Piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass


def encode_board(board: chess.Board,
                 use_reachability: bool = True,
                 use_attack: bool = True,
                 use_defense: bool = True,
                 use_ray_attack: bool = True) -> str:
    base_board_encoding = ""
    closure_encodings = ""
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        base_board_encoding += f"{piece.symbol()}{square}"

        if use_reachability:
            r_closure_enc = reachability_closure(board, piece)
            closure_encodings += f"{r_closure_enc}\n"
        if use_attack:
            a_closure_enc = attack_closure(board, piece)
            closure_encodings += f"{a_closure_enc}\n"
        if use_defense:
            d_closure_enc = defense_closure(board, piece)
            closure_encodings += f"{d_closure_enc}\n"
        if use_ray_attack:
            x_closure_enc = ray_attack_closure(board, piece)
            closure_encodings += f"{x_closure_enc}\n"

    return f"{base_board_encoding}\n{closure_encodings}"


def index_games(games: typing.List[chess.pgn.Game], num_skip=12):
    """
    Base algorithm of the paper
    games: list of games
    """
    pass


def retrieve(board: chess.Board):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = ""
    pass

# TODO test max 1 state retrieved per game

# TODO: Board matrix as dictionary
