import pandas as pd
import string

import General_Functions as Gf


def datacite_date_1st_call(date_range):
    url='https://api.datacite.org/dois?query=created:['+date_range+']&page[cursor]=1&page[size]=1000'

    return url


def datacite_date(date):
    date_range=date+'%20TO%20'+date

    return date_range


def datacite_clean(result):
    print("Cleaning DataCite Results...")
    print("   Renaming columns...")
    renamed_result=result.rename(columns={'attributes.doi': 'DOI',
                                          'attributes.creators': 'Authors',
                                          'attributes.titles': 'Article Title',
                                          'attributes.publisher': 'Publisher',
                                          'attributes.subjects': 'Subject',
                                          'attributes.contributors': 'Contributors',
                                          'attributes.language': 'Language',
                                          'attributes.types.citeproc': 'Article Type',
                                          'attributes.descriptions': 'Description',
                                          'attributes.container.title': 'Journal Title',
                                          'attributes.url': 'Link'
                                          })
    print("   Renaming complete")
    print("   Dropping unwanted columns...")
    dropped_result=renamed_result.drop(columns=['id',
                                                'type',
                                                'attributes.identifiers',
                                                'attributes.publicationYear',
                                                'attributes.dates',
                                                'attributes.types.ris',
                                                'attributes.types.bibtex',
                                                # 'created',
                                                # 'page',
                                                # 'is-referenced-by-count',
                                                # 'prefix',
                                                # 'volume',
                                                # 'member',
                                                # 'deposited',
                                                # 'score',
                                                # 'issue',
                                                # 'journal-issue',
                                                # 'ISSN',
                                                # 'issn-type'
                                                ])

    print("   Dropping complete")

    print("   Adding missing columns...")
    dropped_result.insert(column="Source", loc=0, value="DateCite")
    dropped_result.insert(column="Journal Country", loc=0, value="")
    dropped_result.insert(column="Keywords", loc=0, value="")
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

    print("DataCite Cleaning Complete")

    return reordered_result


def datacite_search(date):
    total_pages=1
    page_number=1

    date_range=date+'%20TO%20'+date

    if page_number == 1:
        print('Calling Datacite Api for Entries Created on '+str(date))

        first_response=Gf.api_call(datacite_date_1st_call(datacite_date(date)))

        url=first_response.json()["links"]["next"]

        total_pages=first_response.json()["meta"]["totalPages"]
        total_docs=first_response.json()["meta"]["total"]
        print('Total of '+str(total_pages)+' pages to collect, for '+str(total_docs)+' total docs')

        print('Storing page '+str(page_number)+'/'+str(total_pages))

        # print(pd.json_normalize(first_response.json()["data"]))

        result=pd.json_normalize(first_response.json()["data"])
        result =[''.join(c for c in s if c not in string.punctuation) for s in result]
        page_number+=1

    while 1<page_number<=total_pages:
        print('Calling for page '+str(page_number))
        try:
            loop_response=Gf.api_call(url)
            url=loop_response.json()["links"]["next"]
            print('Storing page '+str(page_number)+'/'+str(total_pages))
            new_data=pd.json_normalize(loop_response.json()["data"])
            new_data=[''.join(c for c in s if c not in string.punctuation) for s in new_data]
            result=pd.concat([result, new_data])

        except:
            print('All pages collected')

        page_number+=1

    result=datacite_clean(result)

    return result

# datacite_search(date).to_csv("test2.csv")


# result = pd.json_normalize(response.json()["data"])
#
# print("Number of DataCite Results: "+str(len(result)))
#
# print(result)
#
# return result


# results = []
#
# results.append(response.json())


# results = [item for sublist in results for item in sublist]
# results = pd.DataFrame(results)


# results = pd.Series(response.json()).to_frame()

# results = pd.Series(flatten_json_iterative_solution(response.json())).to_frame()

# print(results)


# results.head(30)

# print(flatten_json_iterative_solution(response.json()))

# results = pd.DataFrame(flatten_json_iterative_solution(response.json()))
#
# print(results)

# results = []
#
# results.append(response)
# results = [item for sublist in results for item in sublist]
# results = pd.DataFrame(results)
#
# print(response.text)
#
# try:
#     df=pd.read_json(response)
# except:
#     df=pd.read_json(response.json)


# import requests
# import json
# import pandas as pd
# from pandas.io.json import json_normalize
#
# # url = "https://api.test.datacite.org/activities"
#
# # headers = {"Accept": "application/vnd.api+json"}
#
# # response = requests.request("GET", url, headers=headers)
# #
#
#
#
#
# def datacite_search(date):
#     results = []
#     # for term in tqdm(search_terms):
#
#     date_range = date + '%20TO%20' + date
#
#     url='https://api.datacite.org/dois?query=created:['+date_range+']&page[number]=1&page[size]=1000'
#
#     headers={"Accept": "application/vnd.api+json"}
#
#     r=requests.request("GET", url, headers=headers)
#
#     content=json.loads(r.text)
#
#     df = pd.read_json(content)
#
#     print(df)
#
#     # results.append(pd.DataFrame([content]))
#
#     # print(r.json())
#     # print(response.text)
#
#     # results.append(response)
#     # results = [item for sublist in results for item in sublist]
#     # results = pd.DataFrame(results)
#
#     # data=r.json()
#     # # df=pd.json_normalize(data) - only gives 1 row
#     # # df = pd.DataFrame(data) - mixing dicts with non-series may lead to ambiguous ordering
#     # df = pd.read_json(data)
#
#     #
#     # with open(r) as data_file:
#     #     d=json.load(data_file)
#     #
#     # df=json_normalize(d).assign(**d['status'])
#     # print(df)
#     #
#     # df=pd.DataFrame.from_dict(r)
#
#
#
#     # results.append(search)
#     # results = [item for sublist in results for item in sublist]
#     # results = pd.DataFrame(results)
#     #
#     # # Drop all rows not in timeframe
#     # #results = results[results["published"]# > cutoff_date]
#     # print("Number of Datacite Results: " + str(len(results)))
#     #
#     # print(results)
#
#     # Deduplicate
#     # results = results.drop_duplicates(subset=["id"])
#     # # print("Number of CrossRef Results after removing duplicates: " + str(len(results)))
#     #
#     # df=pd.concat(results, ignore_index=True)
#     df.to_csv('stop_loc1.csv')
#     return df
#
# print(datacite_search('2020-12-10'))
#
