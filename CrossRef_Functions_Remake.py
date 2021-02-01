import pandas as pd
import string
import numpy as np
import General_Functions as Gf


def cr_url(date, loop):
    url = 'https://api.crossref.org/works?filter=from-pub-date:'+date+',until-pub-date:'+date+',type:journal-article&rows=1000&offset='+str(loop)+''
    return url

def cr_clean(result):
    print("Cleaning CR Results...")
    print("   Missing Abstract Population...")


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


def cr_search(date):
    print('Calling CR Api for Entries Created on '+str(date))

    loop = 0
    repeat = 0
    while loop <= repeat:

        response=Gf.api_call(cr_url(date, loop))

        if loop == 0:
            total_docs=response.json()["message"]["total-results"]
            print('Total docs to collect: '+str(total_docs))
            if total_docs > 1000:
                import math
                repeat = math.ceil(total_docs/1000)
                if repeat > 10:
                    print('Implement cursor')
            print('Collecting in batches of 1000, therefore ' + str(repeat - 1) + ' cycles remaining')
            
            result=pd.json_normalize(response.json()["message"]["items"])
        print('Processing Loop:' + str(loop))
        new_data = pd.json_normalize(response.json()["message"]["items"])
        result = pd.concat([result, new_data])

        loop+=1

    print('Main Done')

    print(result.abstract)

    fillna =result.abstract.fillna('')
    cleaning = fillna.to_numpy()

    np_where=np.where(cleaning == '')

    list_empty_values=np_where[0]

    print(list_empty_values)

    loop=0
    while loop<10:
        print('Populating abstract of document number ' + str(loop))
        result.abstract.iat[list_empty_values[loop]] = Gf.doi_to_abstract(result.DOI.iat[list_empty_values[loop]])

        loop+=1

    print('10 Cleaning Complete')

    result.to_csv('pidgon.csv')

        
        


        # try:
        #     url=first_response.json()["next"]
        # except:
        #     print(' next didnt work - check for pagenation')
        # 
        # last_page_url=str(first_response.json()["last"])
        # total_pages=last_page_url[last_page_url.find("page=")+5]
        # total_docs=first_response.json()["total"]
        # 
        # if total_pages != 1:
        #     print(' Total of '+str(total_pages)+' pages to collect, for '+str(total_docs)+' total docs')
        # 
        # print('   Storing page '+str(page_number)+'/'+str(total_pages))
        # 
        # # print(pd.json_normalize(first_response.json()["data"]))
        # 
        # 
        # result=[''.join(c for c in s if c not in string.punctuation) for s in result]
        # page_number+=1

    # while 1<int(page_number)<=int(total_pages):
    #     print('   Calling for page '+str(page_number))
    #     try:
    #         loop_response=Gf.api_call(url)
    #         url=loop_response.json()["next"]
    #         print('   Storing page '+str(page_number)+'/'+str(total_pages))
    #         new_data=pd.json_normalize(loop_response.json()["results"])
    #         new_data=[''.join(c for c in s if c not in string.punctuation) for s in new_data]
    #         result=pd.concat([result, new_data])
    # 
    #     except:
    #         print('exception in try loop')
    # 
    #     print('All pages collected')
    #     page_number+=1

    # result=doaj_clean(result)

    return result

cr_search('2020-01-15')

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
