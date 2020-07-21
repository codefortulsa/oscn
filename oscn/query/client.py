from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from decouple import config


OSCN_API_URL = "https://stage.oscn.net/api"


OSCN_API_ACCESS_KEY = config('OSCN_API_ACCESS_KEY')


client = Elasticsearch(OSCN_API_URL,
                       api_key=OSCN_API_ACCESS_KEY)
