import json
import os

import argparse
import pysolr

import indexing
import solr_util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', dest='delete', action='store_const', const=True, default=False)
    parser.add_argument('-f', '--filenames', nargs="*", type=str, help="Filenames of the PGN files to index",
                        dest='filenames', default=[])
    parser.add_argument('--commit-interval', type=int, default=1000, dest='commit_interval')

    args = parser.parse_args()

    solr = solr_util.get_solr_instance()
    if args.delete:
        indexing.delete_all_documents(solr)
        if os.path.isfile("in_progress.json"):
            os.remove("in_progress.json")

    in_progress = None
    if os.path.isfile("in_progress.json"):
        with open("in_progress.json", "r") as in_progress_file:
            try:
                in_progress = json.loads(in_progress_file.read())
            except Exception as e:
                print("Could not load in_progress file. Skipping it.")

    if len(args.filenames):

        indexed = False
        nr_retries = 0
        while not indexed and nr_retries < 5:
            try:

                if solr.ping():
                    nr_retries = 0

                indexing.index_games(solr, args.filenames, 24, commit_interval=args.commit_interval,
                                     in_progress=in_progress)
                indexed = True
            except pysolr.SolrError as e:
                print("Solr Error has occurred. Restarting.")
                nr_retries += 1
    pass


if __name__ == "__main__":
    main()
