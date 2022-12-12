import pysolr


def get_solr_instance() -> pysolr.Solr:
    return pysolr.Solr('http://localhost:8983/solr/chessGames', always_commit=False, timeout=10)
