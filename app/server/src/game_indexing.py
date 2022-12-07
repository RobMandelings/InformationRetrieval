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


def reachability_closure(board: chess.Board, piece) -> typing.Dict[str, float]:
    """
    Computes the reachability closure of a piece on the given board
    """
    pass


def attack_closure(board: chess.Board, piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass


def defense_closure(board: chess.Board, piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass


def ray_attack_closure(board: chess.Board, piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass


def encode_board(board: chess.Board) -> str:
    for row in reversed(range(1, 9)):
        for col in range(ord('A'), ord('H')):
            pass


def index_games(games: typing.List[chess.pgn.Game], num_skip:int = 12):
    """
    Base algorithm of the paper
    games: list of games
    """
    documents = [] # TODO instead of return list add to documents index
    for g in games:
        # numskip
        board = g.board()
        for move in g.mainline_moves():
            board.push(move)
            brdenc = encode_board(board)
            documents.append(brdenc)

    return documents


# Test for index_games
pgn = open("example_games/game.pgn")
game = chess.pgn.read_game(pgn)
games = [game]
index_games(games)


def retrieve(board: chess.Board):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = ""
    pass

# TODO test max 1 state retrieved per game

# TODO: Board matrix as dictionary

# TODO: document the board encoding from paper

