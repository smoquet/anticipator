from form.models import *
import unicodedata

def unicodetostring(unicode):
    string_out = unicodedata.normalize('NFKD', unicode).encode('ascii','ignore')
    return string_out

def db_event_search(event_query):
    '''
    takes a query and returns a list of events as id:name key_value_pairs
    '''
    search_results = Events.objects.filter(name__icontains=event_query)
    search_results_values = search_results.values()
    # print 'search_results_values = ', search_results_values
    # initialise result list
    search_result_key_value_pairs = []
    # create a list with the names of events as results
    for x in search_results_values:
        search_result_key_value_pairs.append([x['id'], x['name']])

    # print 'search_result_key_value_pairs = ', search_result_key_value_pairs
    return search_result_key_value_pairs

def db_search_by_id(event_query):
    '''
    takes an event id and returns all the db columns as key value pairs
    '''
    search_results = Events.objects.filter(id=event_query)
    search_results_values = search_results.values()
    print 'search_results_values = ', search_results_values
    # initialise result list
    dictonary_unicode = search_results_values[0]
    for key in dictonary_unicode.keys():
        if type(dictonary_unicode[key]) == unicode:
            dictonary_unicode[key] = unicodetostring(dictonary_unicode[key])
    # print dictonary_unicode
    return dictonary_unicode