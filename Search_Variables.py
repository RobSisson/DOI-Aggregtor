

# Program to collect and merge information around journal articles from a variety of open sources

# Variables

# Date
# Please insert in yyyy-mm-dd format
date = "2021-01-17"

# Databases
# There are several different databases which can be searched using this library.
# The databases, with corresponding ID (bracketed) which are to be used in database selection, can be found below:
# CrossRef (cr) - https://www.crossref.org/about/ //  API documentation: https://github.com/CrossRef/rest-api-doc
# DataCite (dc) - https://datacite.org/value.html //  API documentation: https://support.datacite.org/docs/api
# Directory of Open Access Journals (doaj) - https://doaj.org/about/ //  API documentation: https://doaj.org/api/v2/docs

databases = {
    # Please insert a 1 to include, and a 0 to omit, the corresponding database with the next search
    "cr": 1,
    "dc": 1,
    "doaj": 1
}



# Merging Data
# As will be assumed, the data being returned from each of the above APIs has some similarities in content,
# but there is still a significant amount of differences in column titles and content.

# Due to this, there are several different dictionary pairs below which can be used to adjust what data is collected
# from each database, and how to merge it together with the content from other databases. Please customise this at
# at will, using the api documentation where required, though this can get a little complicated so be cautious for
# obvious reasons.

# Due to the complexity of this, a 'recommended_build' option is found below. This will override any alterations made
# to the dictionaries following this, so be sure to set this to 0 if you want to customise the data which is collected
# and the way it is merged.

recommended_build = 1

# The following dictionaries will be split into a global dictionary (global_fields) and then an individual dictionary
# corresponding to each of the databases, containing the fields which are specific to that database.

global_fields = [

]

cr_fields = {

}

dc_fields = {

}

doaj_fields = {

}


# ### Enter your search terms here, list can be as long as you like ###
# search_terms = ['computer supported learning',
# 'computer-supported learning',
# 'intelligent tutoring system',
# 'intelligent teaching system',
# 'artificial tutoring system',
# 'adaptive teaching',
# 'educational technology',
# 'elearning',
# 'e-learning',
# 'pedagogical agent',
# 'educational data mining',
# 'learning analytics',
# 'automatic essay evaluation',
# 'automatic essay scoring',
# 'adaptive educational hypermedia',
# 'adaptive learning spaces',
# 'learning management system',
# 'educational content management']


# Use of merged response
# Changing the below variables will do...well, what it says on the tin

results_use = {
    "export_to_csv": 1,
    "print_results": 1
}

# Export to Directory
directory = r'C:\Users\rob_s\PycharmProjects\systemo\Storage'


# date = '2020-12-25'
#
# print(f'Starting Search of DOAJ for Journals Released on '+date)
# # All results are saved to abstracts.csv #
# data_doaj = doaj_search(date)
# print(data_doaj)
# print('Cross Ref search complete')
# print('Exporting to CSV...')
# data_doaj.to_csv(f"DOAJ - "+date+".csv")
# print('Export Complete')


# print(f'Starting Search of Cross Ref for Journals Released on '+date)
# # All results are saved to abstracts.csv #
# data_cross_ref = cross_ref_search(date)
# print('Cross Ref search complete')
# print('Exporting to CSV...')
# data_cross_ref.to_csv(f"cross_ref-1-"+date+".csv")
# print('Export Complete')
#
#
# print(f'Starting Search of Datacite for Journals Released on '+date)
# data_datacite = datacite_search(date)
# print('Data Cite search complete')
# print('Exporting to CSV...')
# data_datacite.to_csv(f"datacite-1-"+date+".csv")
# print('Export Complete')


# data = pd.DataFrame.append(data_cross_ref, data_datacite)
#
# print(data)

# data.to_csv("abstracts1.csv")