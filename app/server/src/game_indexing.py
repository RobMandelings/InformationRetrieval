import io
import typing

import chess.pgn
import pysolr

import encoding


def get_solr_instance() -> pysolr.Solr:
    return pysolr.Solr('http://localhost:8983/solr/chessGames', always_commit=False, timeout=10)


def index_games(games_pgn_str: typing.List[str], num_skip: int = 24):
    """
    Base algorithm of the paper
    games: list of games
    """

    solr = get_solr_instance()

    for (game_nr, game_str) in enumerate(games_pgn_str):
        g = chess.pgn.read_game(io.StringIO(game_str))
        board = g.board()
        for (move_nr, move) in enumerate(g.mainline_moves()):
            if move_nr > num_skip:
                board_encoding = encoding.encode_board(board)

                solr.add([
                    {
                        "id": int(f"{game_nr}{move_nr}"),
                        "game": game_str,
                        "game_id": game_nr,
                        "move_nr": move_nr,
                        "board": board_encoding['board'],
                        "reachability": board_encoding["reachability"],
                        "attack": board_encoding["attack"],
                        "defense": board_encoding["defense"],
                    },
                ])
                # TODO add "game" field for retrieval of document

            board.push(move)
            # https://pypi.org/project/pysolr/#description

    solr.commit()


# Test for index_games
game_str = open("example_games/game.pgn").read()
game2_str = open("example_games/game2.pgn").read()
game3_str = open("example_games/game3.pgn").read()
game4_str = open("example_games/game4.pgn").read()
games = [game_str, game2_str, game3_str, game4_str]


# index_games(games, num_skip=0)


def write_fen_notations(games):
    with open('example_games/games_fen.txt', 'w+') as output_file:
        for game_str in games:
            game = chess.pgn.read_game(io.StringIO(game_str))
            board = game.board()
            for (move_nr, move) in enumerate(game.mainline_moves()):
                output_file.write(f"{board.fen().split()[0]}\n")
                board.push(move)
            output_file.write('\n')


write_fen_notations(games)


# index_games(games, num_skip=0)


def retrieve(board: chess.Board):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = encoding.encode_board(board)
    solr = get_solr_instance()

    query = f'board:({board_encoding["board"]}) '
    if board_encoding["reachability"]:
        query += f'reachability:({board_encoding["reachability"]}) '
    if board_encoding["attack"]:
        query += f'attack:({board_encoding["attack"]}) '
    if board_encoding["defense"]:
        query += f'defense:({board_encoding["defense"]}) '

    result = solr.search(
        query,
        **{
            "fl": "id,game,score,move_nr",
            "group": "true",
            "group.field": "game_id"
        })

    groups = result.grouped['game_id']['groups']
    documents = list(map(lambda group: group['doclist']['docs'][0], groups))

    # TODO improve checking
    assert groups, "no results were found"
    return documents

# TODO test max 1 state retrieved per game

# TODO: document the board encoding from paper
