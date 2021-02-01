### Data Collection & Management Packages ###
import requests
import json
import pandas as pd
import numpy as np

# ### Time Management & Monitoring Packages ###
# import time
# from time import sleep
# from tqdm import tqdm

### Internal Packages ###
import Search_Variables as Sv
import CrossRef_Functions_Old_Version_Using_Crossref_Restful as Cr
import Datacite_Functions as Dc
import DOAJ_Functions as Doaj


def api_call(url):
    # print(url)
    return requests.request("GET", url)


def collect_data():
    result_df_created=0

    if Sv.databases["cr"] == 1:
        result=Cr.cross_ref_search(Sv.date)
        result_df_created+=1

    if Sv.databases["dc"] == 1:
        if result_df_created == 0:
            result=Dc.datacite_search(Sv.date)
            result_df_created+=Sv
        else:
            result=pd.concat([result, Dc.datacite_search(Sv.date)])

    if Sv.databases["doaj"] == 1:
        if result_df_created == 0:
            result=Doaj.doaj_search(Sv.date)
            result_df_created+=1
        else:
            result=pd.concat([result, Doaj.doaj_search(Sv.date)])

    if Sv.results_use["export_to_csv"] == 1:
        result.to_csv(convert_to_csv(Sv.date), sep='\t', encoding='utf-8', index=False)
        print('CSV Created')
    if Sv.results_use["print_results"] == 1:
        print(result)


def convert_to_csv(date):
    name="Journal_Search"
    if Sv.databases["cr"] == 1:
        Cr="Cr"
        name=".".join((name, Cr))

    if Sv.databases["dc"] == 1:
        Dc="Dc"
        name=".".join((name, Dc))

    if Sv.databases["doaj"] == 1:
        Doaj="Doaj"
        name=".".join((name, Doaj))

    name=" - ".join((name, date))

    import os
    # path=r"C:\Users\rob_s\PycharmProjects\systemo\Storage"
    output_file=os.path.join(Sv.directory, name+".csv")
    print('CSV Path Created')
    return output_file



def doi_to_abstract_semantic(doi):
    sem_url='https://api.semanticscholar.org/v1/paper/'+str(doi)
    response=api_call(sem_url)
    parsed=response.json()["references"]
    print(json.dumps(parsed, indent=4, sort_keys=True))
    result=pd.json_normalize(parsed)

    return result.to_csv('reftest.csv')


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr=[]

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values=extract(obj, arr, key)
    return values


class ReturnValue(object):
    __slots__=["Abstract", "Fields", "Topics"]

    def __init__(self, Abstract, Fields, Topics):
        self.Abstract=Abstract
        self.Fields=Fields
        self.Topics=Topics


def doi_to_key_info(doi):
    sem_url='https://api.semanticscholar.org/v1/paper/'+str(doi)
    response=api_call(sem_url)
    parsed=response.json()

    return ReturnValue(parsed["abstract"], parsed["fieldsOfStudy"], parsed["topics"])

