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


def encode_piece_at(piece, square):
    assert piece
    assert 0 <= square <= chess.SQUARES[-1]
    return f"{piece.symbol()}{chess.SQUARE_NAMES[square]}"


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

    base_board_encoding = " ".join(base_board_list)
    return f"{base_board_encoding}\n{closure_encodings}"


def index_games(games: typing.List[chess.pgn.Game], num_skip: int = 24):
    """
    Base algorithm of the paper
    games: list of games
    """
    documents = []  # TODO instead of return list add to documents index
    for g in games:
        board = g.board()
        for (move_nr, move) in enumerate(g.mainline_moves()):
            if move_nr > num_skip:
                board_encoding = encode_board(board, False, False, False, False)

                solr = pysolr.Solr('http://localhost:8983/solr/chessGames', always_commit=True, timeout=10)
                solr.ping()

                result = solr.search(
                    'board:(Ra1 Ke1 Rh1 Pa2 Pb2 Pf2 Pg2 Ph2 Pc3 Pd3 Qf3 qe5 pc6 Ne6 bg6 pa7 pb7 be7 pg7 ph7 ra8 ke8 rh8)',
                    **{
                        "fl": "id,game_id,score,board",
                        "group": "true",
                        "group.field": "game_id"
                    })
                response = result.raw_response['grouped']['game_id']['']
                doc_id = response['numFound']

                solr.add([
                    {
                        "id": doc_id,
                        "game_id": 0,
                        "move_nr": move_nr,
                        "board": board_encoding,
                    },
                ])
                # TODO add "game" field for retrieval of document

            board.push(move)
            # https://pypi.org/project/pysolr/#description

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
    board_encoding = encode_board(board, False, False, False, False)
    # add additional info to encoding with closures
    # retrieve from index (return for test)
    return board_encoding

# TODO test max 1 state retrieved per game

# TODO: Board matrix as dictionary

# TODO: document the board encoding from paper
