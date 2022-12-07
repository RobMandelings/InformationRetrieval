import enum
import typing

import chess.pgn
import pysolr


class Closure(enum.Enum):
    Reachability = '|'
    Attack = '>'
    Defense = '<'
    RayAttack = '='


def encode_closure(closure: typing.Dict[str, float], closure_type: Closure):
    closure_encodings = map(lambda pair: f"{pair[0]}{closure_type.value}{pair[1]}", list(closure.items()))
    return " ".join(closure_encodings)


# chess.square_distance() is chebychev distance
def reachability_closure(board: chess.Board, square: int) -> typing.Dict[str, float]:
    """
    Computes the reachability closure of a piece on the given board
    """
    piece = board.piece_at(square)
    square_name = chess.square_name(square)
    legal_moves_list = list(board.legal_moves)
    possible_moves = [move for move in legal_moves_list if move.uci()[:2] == square_name]
    closure = {}
    for move in possible_moves:
        d = chess.square_distance(square, chess.parse_square(move.uci()[2:]))
        weight = 1 - ((7*d)/64)
        closure[move.uci()] = weight

    return closure


pgn = open("example_games/game.pgn")
game = chess.pgn.read_game(pgn)
board = game.board()

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


def encode_piece_at(piece, square):
    assert piece
    assert 0 <= square <= chess.SQUARES[-1]
    return f"{piece.symbol()}{chess.square_name(square)}"


def encode_board(board: chess.Board,
                 use_reachability: bool = True,
                 use_attack: bool = True,
                 use_defense: bool = True,
                 use_ray_attack: bool = True) -> str:
    base_board_list = list()
    closure_encodings = ""
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            base_board_list.append(encode_piece_at(piece, square))

            if use_reachability:
                r_closure_enc = reachability_closure(board, square)
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

    base_board_encoding = " ".join(base_board_list)
    return f"{base_board_encoding}\n{closure_encodings}"


def index_games(games: typing.List[chess.pgn.Game], num_skip: int = 24):
    """
    Base algorithm of the paper
    games: list of games
    """
    for g in games:
        board = g.board()
        for (i, move) in enumerate(g.mainline_moves()):
            board.push(move)
            if i + 1 > num_skip:
                board_encoding = encode_board(board, True, False, False, False)

                solr = pysolr.Solr('http://localhost:8983/solr/chessGames', always_commit=True, timeout=10)
                solr.ping()

                solr.add([
                    {
                        "id": "doc_1",
                        "title": "A test document",
                    },
                    {
                        "id": "doc_2",
                        "title": "The Banana: Tasty or Dangerous?",
                        "_doc": [
                            {"id": "child_doc_1", "title": "peel"},
                            {"id": "child_doc_2", "title": "seed"},
                        ]
                    },
                ])
                # https://pypi.org/project/pysolr/#description


# Test for index_games
# pgn = open("example_games/game.pgn")
# game = chess.pgn.read_game(pgn)
# games = [game]
# index_games(games)


def retrieve(board: chess.Board):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = encode_board(board, False, False, False, False)
    # add additional info to encoding with closures
    # retrieve from index (return for test)
    return board_encoding

# TODO test max 1 state retrieved per game

# TODO: Board matrix as dictionary

# TODO: document the board encoding from paper
