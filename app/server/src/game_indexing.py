import io
import os
import sys
import typing

import chess.pgn
import pysolr
from tqdm.auto import tqdm

import closures
import encoding


class MovePushException(Exception):
    pass


def get_solr_instance() -> pysolr.Solr:
    return pysolr.Solr('http://localhost:8983/solr/chessGames', always_commit=False, timeout=10)


def create_documents(game_id, game_string, num_skip):
    game = chess.pgn.read_game(io.StringIO(game_string))
    board = game.board()
    documents = []

    for (move_nr, move) in enumerate(game.mainline_moves()):
        if move_nr > num_skip:
            board_encoding = encoding.encode_board(board, list(closures.Metric.__members__.values()))

            documents.append({
                "id": int(f"{game_id}{move_nr}"),
                "game": game_string,
                "game_id": game_id,
                "move_nr": move_nr,
                "board": board_encoding['board'],
                "reachability": board_encoding['metrics'][closures.Metric.Reachability],
                "attack": board_encoding['metrics'][closures.Metric.Attack],
                "defense": board_encoding['metrics'][closures.Metric.Defense],
            })

        try:
            board.push(move)
        except Exception as e:
            raise MovePushException(
                f"Could not create document for game with game_id {game_id} and move_nr {move_nr}: invalid") from e

    return documents


def index_games(filenames, num_skip: int = 24, delete_previous_docs=False):
    """
    Base algorithm of the paper
    games: list of games
    """

    solr = get_solr_instance()

    if delete_previous_docs:
        solr.delete(q='*:*')
        solr.commit()

    game_id = solr.search('game_id:*').raw_response['response']['numFound']

    for filename in filenames:

        file_size = os.path.getsize(filename) / 1000_000
        file = open(filename)

        game_string = ""

        pbar = tqdm(total=file_size, unit="MB")
        for line in file:
            game_string += line

            if line.startswith("1."):
                try:
                    documents = create_documents(game_id, game_string, num_skip)

                    if len(documents):
                        solr.add(documents)
                        game_id += 1

                except MovePushException as e:
                    print(f"A move push exception occurred for game id {game_id}. This game will not be indexed.")
                    print(e)

                game_string = ""

            pbar.update((sys.getsizeof(line) - sys.getsizeof('\n')) / 1000_000)
        pbar.close()

    solr.commit()


# Test for index_games
# game_file = open("example_games/game.pgn")
# game2_str = open("example_games/game2.pgn").read()
# game3_str = open("example_games/game3.pgn").read()
# game4_str = open("example_games/game4.pgn").read()
# games = [game_str, game2_str, game3_str, game4_str]

index_games(["game_data/lichess_db_standard_rated_2013-01.pgn"], num_skip=24, delete_previous_docs=True)


def write_fen_notations(games):
    with open('example_games/games_fen.txt', 'w+') as output_file:
        for game_str in games:
            game = chess.pgn.read_game(io.StringIO(game_str))
            board = game.board()
            for (move_nr, move) in enumerate(game.mainline_moves()):
                output_file.write(f"{board.fen().split()[0]}\n")
                board.push(move)
            output_file.write('\n')


# write_fen_notations(games)


# index_games(games, num_skip=0)


def retrieve(board: chess.Board, metrics: typing.List[closures.Metric]):
    """
    Retrieves a ranked list of game states provided the query
    TODO retrieve complete games as documents instead of boards
    """
    board_encoding = encoding.encode_board(board, metrics)
    solr = get_solr_instance()

    query = f'board:({board_encoding["board"]}) '
    for metric, enc in board_encoding['metrics'].items():
        if enc:
            query += f'{metric.name.lower()}:({enc}) '

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
