import requests
import pandas as pd



def api_call(url):
    # print(url)
    return requests.request("GET", url)

def OpenAIRE_search(date_range):

    base_url = 'http://api.openaire.eu/search/publications'

    return base_url