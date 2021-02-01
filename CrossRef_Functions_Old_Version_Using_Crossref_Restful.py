from crossref.restful import Works
import pandas as pd
import numpy as np
import seaborn as sns
import string

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure


matplotlib.rcParams['figure.figsize'] = (12,8)

pd.options.mode.chained_assignment = None


works=Works()

def crossref_clean(result):
    print("Cleaning CrossRef Results...")
    print("   Renaming columns...")
    renamed_result=result.rename(columns={'publisher': 'Publisher',
                                          'publisher-location': 'Publisher Location',
                                          'abstract': 'Description',
                                          'type': 'Article Type',
                                          'title': 'Article Title',
                                          'author': 'Authors',
                                          'container-title': 'Journal Title',
                                          'language': 'Language',
                                          'URL': 'Link',
                                          'source': 'Source',
                                          'subject': 'Subject'
                                          })
    print("   Renaming complete")
    print("   Dropping unwanted columns...")
    dropped_result=renamed_result.drop(columns=['indexed',
                                                'reference-count',
                                                'issue',
                                                'license',
                                                'content-domain',
                                                'accepted',
                                                'published-print',
                                                'created',
                                                'page',
                                                'is-referenced-by-count',
                                                'prefix',
                                                'volume',
                                                'member',
                                                'deposited',
                                                'score',
                                                'issue',
                                                'journal-issue',
                                                'ISSN',
                                                'issn-type',
                                                #'edition-number',
                                                'license',
                                                'alternative-id',
                                                'article-number',
                                                'published-online',
                                                #'original-title',
                                                'update-policy',
                                                'reference',
                                                'archive',
                                                'relation',
                                                'subtitle',
                                                'institution',
                                                'posted',
                                                'group-title',
                                                'accepted',
                                                'subtype',
                                                'editor',
                                                #'update-to',
                                                # 'short-title',
                                                # 'review',
                                                # 'chair',
                                                ])

    print("   Dropping complete")

    print("   Adding missing columns...")
    dropped_result.insert(column="Keywords", loc=0, value="")
    dropped_result.insert(column="Contributors", loc=0, value="")
    dropped_result.insert(column="Journal Country", loc=0, value="")
    dropped_result.insert(column="Publisher Location", loc=0, value="")
    print("   Missing columns added")

    print("   Reordering columns...")
    columns=['Article Title',
             'Description',
             'Keywords',
             'Subject',
             'Link',
             'Language',
             'Article Type',
             'Journal Title',
             'Journal Country',
             'Publisher',
             'Publisher Location',
             'Authors',
             'Contributors',
             'DOI',
             'Source']

    reordered_result=dropped_result[columns]
    print("   Reordering complete")

    print("CrossRef Cleaning Complete")

    return reordered_result

def cross_ref_search(date):
    print('Calling CrossRef Api for Entries Created on '+str(date))
    results=[]
    search=works.filter(from_pub_date=date, until_pub_date=date)
    print("Found " + str(search.count()) + " results")

    search = [''.join(c for c in s if c not in string.punctuation) for s in search]

    print("Appending...")
    results.append(search)
    results=[item for sublist in results for item in sublist]
    results=pd.DataFrame(results)

    print("Number of CrossRef results appended: "+str(len(results)))

    # print("CrossRef Results: " + str(results))

    # Deduplicate
    # results = results.drop_duplicates(subset=["id"])
    # print("Number of CrossRef Results after removing duplicates: " + str(len(results)))

    results = crossref_clean(results)

    return results




# def crossref_filter(test,pizza,pie)
#     try print
#
#
#     if test != '':
#         print(test)


# crossref_filter('test','','test')
#
#

# for i in works.filter(from_accepted_date='2020-12-12').select('title, DOI, abstract, reference'):
#     print(i)

#### Ryans below

#
# import pandas as pd
# from tqdm import tqdm
# from crossref.restful import Works
#
#


#
# def cross_ref_search(search_terms, cutoff_date="2010-01-01"):
#     results = []
#     for term in tqdm(search_terms):
#         search = arxiv.query(query=term,
#                 max_results=10000,
#                 start=0,
#                 sort_by="relevance",
#                 sort_order="descending",
#                 prune=True,
#                 iterative=False,
#                 max_chunk_results=1000)
#
#         results.append(search)
#     results = [item for sublist in results for item in sublist]
#     results = pd.DataFrame(results)
#
#     # Drop all rows not in timeframe
#     #results = results[results["published"]# > cutoff_date]
#     print("Number of ArXiv Results: " + str(len(results)))
#
#     # Deduplicate
#     results = results.drop_duplicates(subset=["id"])
#     print("Number of ArXiv Results after removing duplicates: " + str(len(results)))
#
#     return results
