import typing

import chess.pgn


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


pgn = open("example_games/game.pgn")
game = chess.pgn.read_game(pgn)
games = [game]


def index_games(games: typing.List[chess.pgn.Game], num_skip: int = 12):
    """
    Base algorithm of the paper
    games: list of games
    """
    for g in games:
        # numskip
        board = g.board()
        brdenc = None
        for move in g.mainline_moves():
            board.push(move)

def retrieve(board: chess.Board):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    pass

# TODO test max 1 state retrieved per game

# TODO: Board matrix as dictionary

# TODO: document the board encoding from paper


index_games(games)
