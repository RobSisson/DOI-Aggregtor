import pandas as pd
import datetime as dt
from datetime import timedelta
import string

import General_Functions as Gf


def doaj_url(date_range):
    url='https://doaj.org/api/v2/search/articles/created_date%3A%5B'+date_range+'%5D?pageSize=100'

    return url


def doaj_date(date):
    y=str(date)[0:4]
    m=str(date)[5:7]
    d=str(date)[8:10]

    date=dt.date(int(y), int(m), int(d))
    date_2=date-timedelta(days=1)
    date_range=str(date_2)+'%20TO%20'+str(date)
    return date_range


def doaj_clean(result):
    print("Cleaning DOAJ Results...")

    print("   Renaming columns...")
    renamed_result=result.rename(columns={'bibjson.identifier': 'DOI',
                                          'bibjson.author': 'Authors',
                                          'bibjson.title': 'Article Title',
                                          'bibjson.journal.publisher': 'Publisher',

                                          'bibjson.subject': 'Subject',
                                          'bibjson.keywords': 'Keywords',
                                          'bibjson.journal.language': 'Language',

                                          'bibjson.abstract': 'Description',

                                          'bibjson.journal.title': 'Journal Title',
                                          'bibjson.journal.country': 'Journal Country',

                                          'bibjson.link': 'Link'
                                          })
    print("   Renaming complete")

    print("   Dropping unwanted columns...")
    dropped_result=renamed_result.drop(columns=['id',
                                                'created_date',
                                                'last_updated',
                                                'bibjson.end_page',
                                                'bibjson.year',
                                                'bibjson.journal.volume',
                                                'bibjson.journal.number',
                                                'bibjson.journal.issns',
                                                'bibjson.month',
                                                'bibjson.start_page',
                                                'admin.seal',
                                                ])
    print("   Dropping complete")

    print("   Adding missing columns...")
    dropped_result.insert(column="Source", loc=0, value="DOAJ")
    dropped_result.insert(column="Contributors", loc=0, value="")
    dropped_result.insert(column="Article Type", loc=0, value="")
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

    print("DOAJ Cleaning Complete")
    return reordered_result


def doaj_search(date):
    total_pages=1
    page_number=1

    if page_number == 1:
        print('Calling DOAJ Api for Entries Created on '+str(date))

        first_response=Gf.api_call(doaj_url(doaj_date(date)))

        try:
            url=first_response.json()["next"]
        except:
            print(' Only one page to collect')

        last_page_url=str(first_response.json()["last"])
        total_pages=last_page_url[last_page_url.find("page=")+5]
        total_docs=first_response.json()["total"]

        if total_pages != 1:
            print(' Total of '+str(total_pages)+' pages to collect, for '+str(total_docs)+' total docs')

        print('   Storing page '+str(page_number)+'/'+str(total_pages))

        # print(pd.json_normalize(first_response.json()["data"]))

        result=pd.json_normalize(first_response.json()["results"])
        result=[''.join(c for c in s if c not in string.punctuation) for s in result]
        page_number+=1

    while 1<int(page_number)<=int(total_pages):
        print('   Calling for page '+str(page_number))
        try:
            loop_response=Gf.api_call(url)
            url=loop_response.json()["next"]
            print('   Storing page '+str(page_number)+'/'+str(total_pages))
            new_data=pd.json_normalize(loop_response.json()["results"])
            new_data=[''.join(c for c in s if c not in string.punctuation) for s in new_data]
            result=pd.concat([result, new_data])

        except:
            print('exception in try loop')

        print('All pages collected')
        page_number+=1

    result=doaj_clean(result)

    return result

# pizza = pd.read_csv(".Doaj - 2020-12-25.csv")
#
# print(pizza.columns.tolist())
# pizza.drop(['Unnamed: 0'], axis=1)
# pizza.drop(columns=['id',
#                          'created_date',
#                          'last_updated',
#                          'bibjson.journal.volume',
#                          'bibjson.journal.number',
#                          'bibjson.journal.issns',
#                          'bibjson.month',
#                          'bibjson.start_page',
#                          'admin.seal',
#                          ])
# print(pizza)

# datacite_search(date).to_csv("test2.csv")

# Cleaning for DOAJ Journals (not specific articles)
# Interesting info about the review process
# result.rename(columns={'attributes.doi': 'DOI',
#                        'attributes.creators': 'Authors',
#                        'bibjson.title': 'Article Title',
#                        'bibjson.publisher.name': 'Publisher',
#                        'bibjson.publisher.country': 'Publisher Country',
#                        'bibjson.subject': 'Subject',
#                        'bibjson.keywords': 'Keywords',
#                        'bibjson.language': 'Language',
#
#                        'attributes.descriptions': 'Description',
#
#                        'bibjson.editorial.review_url': 'Review Process Details',
#                        'bibjson.editorial.board_url': 'Review Board',
#                        'bibjson.editorial.review_process': 'Review Process',
#                        'bibjson.institution.name': '',
#                        'bibjson.institution.country': '',
#
#                        'bibjson.ref.journal': 'Journal Link',
#
#
#
#
#
#                        'attributes.url': 'Link'
#                        })
# result.drop(columns=['id',
#                      'created_date',
#                      'last_updated',
#                      'bibjson.boai',
#                      'bibjson.eissn',
#                      'bibjson.pissn',
#                      'bibjson.publication_time_weeks',
#                      'bibjson.apc.has_apc',
#                      'bibjson.apc.url',
#                      'bibjson.article.license_display_example_url',
#                      'bibjson.article.orcid',
#                      'bibjson.article.i4oc_open_citations',
#                      'bibjson.article.license_display',
#                      'bibjson.copyright.author_retains',
#                      'bibjson.copyright.url',
#                      'bibjson.deposit_policy.has_policy',
#                      'bibjson.editorial.review_url',
#                      'bibjson.editorial.board_url',
#                      'bibjson.editorial.review_process',
#                      'bibjson.other_charges.has_other_charges',
#                      'bibjson.pid_scheme.has_pid_scheme',
#                      'bibjson.pid_scheme.scheme',
#                      'bibjson.plagiarism.detection',
#                      'bibjson.plagiarism.url',
#                      'bibjson.preservation.has_preservation',
#                      'bibjson.ref.oa_statement',
#                      'bibjson.ref.aims_scope',
#                      'bibjson.ref.author_instructions',
#                      'bibjson.ref.license_terms',
#                      'bibjson.waiver.has_waiver',
#                      'bibjson.license',
#                      'admin.seal',
#                      'admin.ticked',
#                      'bibjson.alternative_title',
#                      'bibjson.deposit_policy.url',
#                      'bibjson.deposit_policy.service',
#                      'bibjson.preservation.url',
#                      'bibjson.preservation.service',
#                      ])
