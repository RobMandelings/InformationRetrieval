import argparse

import indexing
import solr_util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', dest='delete', action='store_const', const=True, default=False)
    parser.add_argument('-f', '--filenames', nargs="*", type=str, help="Filenames of the PGN files to index",
                        dest='filenames', default=[])

    args = parser.parse_args()

    solr = solr_util.get_solr_instance()
    if args.delete:
        indexing.delete_all_documents(solr)

    if len(args.filenames):
        indexing.index_games(solr, args.filenames, 24, 1000)
    pass


if __name__ == "__main__":
    main()
