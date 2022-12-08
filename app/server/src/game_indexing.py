import enum
import typing

import chess.pgn
import pysolr


class Closure(enum.Enum):
    Reachability = '|'
    Attack = '>'
    Defense = '<'
    RayAttack = '='


def encode_closure(closure, closure_type: Closure):
    if closure_type is Closure.Reachability:
        # typing.Dict[str, float]
        closure_encodings = map(lambda pair: f"{pair[0]}{closure_type.value}{pair[1]}", list(closure.items()))
        return " ".join(closure_encodings)
    elif closure_type in {Closure.Attack, Closure.Defense}:
        closure_encodings = []
        for (item_nr, item) in enumerate(closure[1]):
            closure_encodings.append(f"{closure[0]}{closure_type.value}{closure[1][item_nr]}")
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
        weight = 1 - ((7 * d) / 64)
        key = board.piece_at(chess.parse_square(move.uci()[:2])).symbol() + move.uci()[2:]
        closure[key] = weight

    return closure


def attack_closure(board: chess.Board, square: int) -> typing.Tuple[str, typing.List[str]]:
    """
    Compute the attack closure of a piece on the given board
    """
    attacked_squares = board.attacks(square)
    attacked_pieces = []
    color = board.color_at(square)
    for attacked_square in attacked_squares:
        if board.piece_at(attacked_square) is not None and color is not board.color_at(attacked_square):
            attacked_pieces.append(board.piece_at(attacked_square).symbol() + chess.square_name(attacked_square))
    closure = (board.piece_at(square).symbol(), attacked_pieces)

    return closure


def defense_closure(board: chess.Board, square: int) -> typing.Tuple[str, typing.List[str]]:
    """
    Compute the defense closure of a piece on the given board
    """
    attacked_squares = board.attacks(square)
    attacked_pieces = []
    color = board.color_at(square)
    for attacked_square in attacked_squares:
        if board.piece_at(attacked_square) is not None and color is board.color_at(attacked_square):
            attacked_pieces.append(board.piece_at(attacked_square).symbol() + chess.square_name(attacked_square))
    closure = (board.piece_at(square).symbol(), attacked_pieces)

    return closure


pgn = open("example_games/game2.pgn")
game = chess.pgn.read_game(pgn)
board = game.board()
for move in game.mainline_moves():
    board.push(move)
test = defense_closure(board, 3)
encoded_closure = encode_closure(test, Closure.Defense)
print(encoded_closure)


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
                a_closure_enc = attack_closure(board, square)
                closure_encodings += f"{a_closure_enc}\n"
            if use_defense:
                d_closure_enc = defense_closure(board, square)
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

# TODO: document the board encoding from paper
