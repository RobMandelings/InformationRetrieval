import enum
import chess.pgn
import typing

"""
This file contains all the closures possible to use to calculate the similarity between chess boards.

Functions reachability_closure, attack_closure, defense_closure are implemented based on the paper: 
Retrieval of Similar Chess Positions.

All the closure implementations return a datastructure containing the right representations for further
encoding which is eventually used in the documents created by the indexing algorithm.

The Closure enum contains all the closures and their corresponding symbols for the encoding.

The encoding implementation can be found in encoding.py.
For more info about closures and encoding we refer to our report.
"""


class Closure(enum.Enum):
    """
    An enum containing all closures and their corresponding symbols used for encoding
    """
    Reachability = '|'
    Attack = '>'
    Defense = '<'
    RayAttack = '='


def reachability_closure(board: chess.Board, square: int) -> typing.Dict[str, float]:
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
    legal_moves_list = list(board.legal_moves)
    possible_moves = [move for move in legal_moves_list if move.uci()[:2] == square_name]
    closure = {}
    for move in possible_moves:
        d = chess.square_distance(square, chess.parse_square(move.uci()[2:]))
        weight = 1 - ((7 * d) / 64)
        key = piece.symbol() + move.uci()[2:]
        closure[key] = weight

    return closure


def attack_closure(board: chess.Board, square: int) -> typing.Tuple[str, typing.List[str]]:
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
            attacked_pieces.append(board.piece_at(attacked_square).symbol() + chess.square_name(attacked_square))
    closure = (board.piece_at(square).symbol(), attacked_pieces)

    return closure


def defense_closure(board: chess.Board, square: int) -> typing.Tuple[str, typing.List[str]]:
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
            attacked_pieces.append(board.piece_at(attacked_square).symbol() + chess.square_name(attacked_square))
    closure = (board.piece_at(square).symbol(), attacked_pieces)

    return closure


def ray_attack_closure(board: chess.Board, piece: chess.Piece) -> typing.Dict[str, float]:
    """
    Compute the attack closure of a piece on the given board
    """
    pass

# pgn = open("example_games/game2.pgn")
# game = chess.pgn.read_game(pgn)
# board = game.board()
# for move in game.mainline_moves():
#     board.push(move)
# test = defense_closure(board, 3)
# encoded_closure = encode_closure(test, Closure.Defense)
# print(encoded_closure)
