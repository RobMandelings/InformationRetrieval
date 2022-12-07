import chess.pgn


def reachability_closure():
    """
    r-closure in the paper
    """
    pass


def alpha_closure():
    """
    Not sure whether to compute the closures attack, defense and x-ray one by one or at once
    """
    pass


pgn = open("example_games/game.pgn")
game = chess.pgn.read_game(pgn)
print(game)


def index_games(games: list):
    """
    Base algorithm of the paper
    games: list of chess board objects (chess library)
    """
    pass


def retrieve(board_matrix):
    """
    Retrieves a ranked list of game states provided the query
    """
    pass

# TODO test max 1 state retrieved per game

# TODO: Board matrix as dictionary