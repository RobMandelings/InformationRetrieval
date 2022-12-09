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
                board_encoding = encoding.encode_board(board, False, False, False, False)
                solr.add([
                    {
                        "id": int(f"{game_nr}{move_nr}"),
                        "game": game_str,
                        "game_id": game_nr,
                        "move_nr": move_nr,
                        "board": board_encoding,
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
index_games(games, num_skip=0)


def retrieve(board: chess.Board):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = encoding.encode_board(board, False, False, False, False)
    solr = get_solr_instance()
    result = solr.search(
        # 'board:(Ra1 Nb1 Bc1 Qd1 Ke1 Bf1 Ng1 Rh1 Pa2 Pb2 Pc2 Pd2 Pf2 Pg2 Ph2 Pe4 pa7 pb7 pc7 pd7 pe7 pf7 pg7 ph7 ra8 nb8 bc8 qd8 ke8 bf8 ng8 rh8)',
        'board:(Ra1 Bc1 Ke1 Bf1 Ng1 Rh1 Pa2 Pb2 Pc2 Pd2 Pf2 Pg2 Ph2 Qf3 Ne4 pc6 pa7 pb7 nd7 pe7 pf7 pg7 ph7 ra8 bc8 qd8 ke8 bf8 ng8 rh8)',
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
