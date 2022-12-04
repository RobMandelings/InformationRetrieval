import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True, timeout=10, auth=None)
