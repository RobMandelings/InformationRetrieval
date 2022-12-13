import io
import json
import os
import sys

import chess.pgn
import pysolr
from tqdm.auto import tqdm

import closures
import encoding


class MovePushException(Exception):
    pass


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


def delete_all_documents(solr_instance: pysolr.Solr):
    solr_instance.delete(q='*:*')
    solr_instance.commit()


def update_progress_json(in_progress: dict):
    with open("in_progress.json", "w+") as in_progress_file:
        in_progress_file.write(json.dumps(in_progress))


def index_games(solr_instance: pysolr.Solr, filenames, num_skip: int = 24,
                commit_interval=100, in_progress: dict = None):
    """
    Base algorithm of the paper
    games: list of games
    :commit_interval: amount of games between commits (in case many games are indexed at once)
    """

    game_id = solr_instance.search('game_id:*').raw_response['response']['numFound']

    for filename in filenames:

        file_size = os.path.getsize(filename) / 1000_000
        file = open(filename)

        game_string = ""

        in_progress = in_progress if in_progress else {}
        resume_at_byte = 0
        if filename in in_progress:
            resume_at_byte = in_progress[filename]
            file.seek(resume_at_byte, 0)
            # pbar.update(resume_at_byte / 1_000_000)

        pbar = tqdm(total=(file_size - resume_at_byte / 1000000), unit="MB")

        line = file.readline()
        while line:
            game_string += line

            if line.startswith("1."):
                try:
                    documents = create_documents(game_id, game_string, num_skip)

                    if len(documents):
                        solr_instance.add(documents)
                        game_id += 1

                        if game_id % commit_interval == 0:
                            solr_instance.commit()
                            in_progress[filename] = file.tell()
                            update_progress_json(in_progress)

                except MovePushException as e:
                    print(f"A move push exception occurred for game id {game_id}. This game will not be indexed.")
                    print(e)

                game_string = ""

            pbar.update((sys.getsizeof(line) - sys.getsizeof('\n')) / 1000_000)
            line = file.readline()

        if filename in in_progress:
            del in_progress["filename"]
        update_progress_json(in_progress)

        pbar.close()

    solr_instance.commit()


# Test for index_games
# game_file = open("example_games/game.pgn")
# game2_str = open("example_games/game2.pgn").read()
# game3_str = open("example_games/game3.pgn").read()
# game4_str = open("example_games/game4.pgn").read()
# games = [game_str, game2_str, game3_str, game4_str]


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

# TODO test max 1 state retrieved per game

# TODO: document the board encoding from paper
