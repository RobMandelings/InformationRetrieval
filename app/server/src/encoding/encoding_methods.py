import enum
import typing
from itertools import chain

import chess.pgn

"""
This file contains all the closures possible to use to calculate the similarity between chess boards.

Functions reachability_closure, attack_closure, defense_closure and ray_attack_closure are implemented based on the 
paper: Retrieval of Similar Chess Positions.

All the closure implementations return a datastructure containing the right representations for further
encoding which is eventually used in the documents created by the indexing algorithm.

The check is not really a closure, but it returns the right representation as well for further encoding.

The Encoding enum contains all the encodings and their corresponding symbols for the encoding.

The encoding implementation can be found in encoding.py.
For more info about closures and encoding we refer to our report.
"""


def encode_piece_at(piece: chess.Piece, square: chess.Square):
    """
    Helper function that encodes a square based on the piece on this square.

    square -> {piece symbol}{square name}

    For example we have a White queen standing on position 2, this will be encoded into Qc1.
    """
    assert piece
    assert 0 <= square <= chess.SQUARES[-1]
    return f"{piece.symbol()}{chess.square_name(square)}"


class EncodingMethod(enum.Enum):
    """
    An enum containing all encoding methods (i.e. closures, check) and their corresponding symbols used for further encoding
    """
    Board = ''
    Reachability = '|'
    Attack = '>'
    Defense = '<'
    RayAttack = '='
    Check = ''

    @staticmethod
    def from_str(metric_name: str):

        if metric_name.lower() == 'board':
            return EncodingMethod.Board
        if metric_name.lower() == 'reachability':
            return EncodingMethod.Reachability
        elif metric_name.lower() == 'attack':
            return EncodingMethod.Attack
        elif metric_name.lower() == 'defense':
            return EncodingMethod.Defense
        elif metric_name.lower() == 'ray_attack':
            return EncodingMethod.RayAttack
        elif metric_name.lower() == 'check':
            return EncodingMethod.Check

        raise ValueError('Could not convert string to metric')


# TODO can be improved: apply mask, nand with moves, ...
# TODO legal moves is expensive, so added as parameter. However could be better
def reachability_closure(board: chess.Board, square: chess.Square, legal_moves_list: list) -> typing.Dict[str, float]:
    """
    Computes the reachability closure of piece p on square (x,y) with a given board:

        r-closure(p,x,y)

    This closure is contains all reachable squares (x',y') of p from (x,y) with a certain weight based
    on a weight function w(p,x,y,x',y')

    This weight function uses the Chebychev distance to calculate the distance between two squares d((x,y),(x',y'))

    :parameter: board: board on which reachability closure is calculated
    :parameter: square: square of which reachability closure is calculated
    :return: closure: reachability closure in a dictionary containing the proper representations for further encoding
    """
    piece = board.piece_at(square)
    square_name = chess.square_name(square)
    possible_moves = [move for move in legal_moves_list if move.uci()[:2] == square_name]
    closure = {}
    for move in possible_moves:
        # TODO maybe mention promotion in paper, update slicing indices to handle the promotion case
        d = chess.square_distance(square, chess.parse_square(move.uci()[2:4]))
        weight = 1 - ((7 * d) / 64)
        key = piece.symbol() + move.uci()[2:4]
        closure[key] = weight

    return closure


def attack_closure(board: chess.Board, square: chess.Square) -> typing.Tuple[str, typing.List[str]]:
    """
    Computes the attack closure of piece p on square (x,y) with a given board:

        a-closure(p,x,y)

    This closure contains all pieces (p') at squares (x',y') that can be attacked by p on (x,y)

    It is important to notice that square (x,y) of p is not included in the computed closure, each
    item in the closure represents a tuple: (p,p',x',y')

    :parameter: board: board on which attack closure is calculated
    :parameter: square: square of which attack closure is calculated
    :return: closure: attack closure in a tuple containing the proper representations for further encoding
    """
    attacked_squares = board.attacks(square)
    attacked_pieces = []
    color = board.color_at(square)
    for attacked_square in attacked_squares:
        if board.piece_at(attacked_square) is not None and color is not board.color_at(attacked_square):
            attacked_pieces.append(encode_piece_at(board.piece_at(attacked_square), attacked_square))
    closure = (board.piece_at(square).symbol(), attacked_pieces)

    return closure


def defense_closure(board: chess.Board, square: chess.Square) -> typing.Tuple[str, typing.List[str]]:
    """
    Computes the defense closure of piece p on square (x,y) with a given board:

        d-closure(p,x,y)

    This closure contains all pieces (p') at squares (x',y') that can be defended by p on (x,y)

    It is important to notice that square (x,y) of p is not included in the computed closure, each
    item in the closure represents a tuple: (p,p',x',y')

    :parameter: board: board on which defense closure is calculated
    :parameter: square: square of which defense closure is calculated
    :return: closure: defense closure in a tuple containing the proper representations for further encoding
    """
    attacked_squares = board.attacks(square)
    attacked_pieces = []
    color = board.color_at(square)
    for attacked_square in attacked_squares:
        if board.piece_at(attacked_square) is not None and color is board.color_at(attacked_square):
            attacked_pieces.append(encode_piece_at(board.piece_at(attacked_square), attacked_square))
    closure = (board.piece_at(square).symbol(), attacked_pieces)

    return closure


def diagonals(coord):
    """
    Helper function returning all the coordinates of the squares on the same diagonal as the square on the given
    coordinates: coord.

    This way of calculating these coordinates was taken from the following stackexchange link:
    https://codereview.stackexchange.com/a/146961

    We used this to simplify our code.
    """
    x, y = coord
    size = 8
    return list(chain(
        [(x, y)],
        zip(range(x - 1, -1, -1), range(y - 1, -1, -1)),
        zip(range(x + 1, size, 1), range(y + 1, size, 1)),
        zip(range(x + 1, size, 1), range(y - 1, -1, -1)),
        zip(range(x - 1, -1, -1), range(y + 1, size, 1)),
    ))


def ray_attack_closure(board: chess.Board, square: chess.Square) -> typing.Tuple[str, typing.List[str]]:
    """
    Computes the ray attack closure of piece p on square (x,y) with a given board:

        x-closure(p,x,y)

    This closure contains all pieces (p') at squares (x',y') that can be 'ray attacked' by p on (x,y)
    A ray attack is a wider way to look at attack.  It not only occurs when a piece is directly attacking another piece,
    but also when it is attacking through other pieces in its way.

    It is important to notice that square (x,y) of p is not included in the computed closure, each
    item in the closure represents a tuple: (p,p',x',y')

    :parameter: board: board on which defense closure is calculated
    :parameter: square: square of which ray attack closure is calculated
    :return: closure: ray attack closure in a tuple containing the proper representations for further encoding
    """
    piece_type = board.piece_type_at(square)
    piece_color = board.color_at(square)
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    ray_attacked_pieces = []
    if piece_type == chess.ROOK or piece_type == chess.QUEEN:
        for i in range(8):
            square_on_rank = chess.square(i, rank)
            square_on_file = chess.square(file, i)
            if board.color_at(square_on_rank) not in [piece_color, None]:
                ray_attacked_pieces.append(encode_piece_at(board.piece_at(square_on_rank), square_on_rank))
            if board.color_at(square_on_file) not in [piece_color, None]:
                ray_attacked_pieces.append(encode_piece_at(board.piece_at(square_on_file), square_on_file))
    if piece_type == chess.BISHOP or piece_type == chess.QUEEN:
        coords_diagonal = diagonals((rank, file))
        for item in coords_diagonal:
            square_on_diagonal = chess.square(item[1], item[0])
            if board.color_at(square_on_diagonal) not in [piece_color, None]:
                ray_attacked_pieces.append(encode_piece_at(board.piece_at(square_on_diagonal), square_on_diagonal))
    closure = (board.piece_at(square).symbol(), ray_attacked_pieces)
    return closure


def check(board: chess.Board, square: chess.Square) -> (bool, chess.Square):
    """
    Determines whether the piece p on square (x,y) is attacking the opponent's king.

    :parameter: board: board on which check is determined
    :parameter: square: square of which check is determined
    :return: attacks_king: boolean whether the piece p on square(x,y) is attacking the king
             representation: if piece p is checking the king, it will give the corresponding representation for further
             encoding, otherwise it will return None
    """
    attacks_king = False
    attacked_squares = board.attacks(square)
    representation = None
    for attacked_square in attacked_squares:
        if board.piece_type_at(attacked_square) == chess.KING and board.color_at(attacked_square) != board.color_at(
                square):
            attacks_king = True
            representation = encode_piece_at(board.piece_at(square), square)

    return attacks_king, representation

#
# pgn = open("example_games/game5.pgn")
# game = chess.pgn.read_game(pgn)
# board = game.board()
# for move in game.mainline_moves():
#     board.push(move)
# ray_closure = ray_attack_closure(board, 33)
