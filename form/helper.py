from form.models import *
import unicodedata
from ast import literal_eval

def unicodetostring(unicode):
    string_out = unicodedata.normalize('NFKD', unicode).encode('ascii','ignore')
    return string_out

def list_to_string_or_back(list_or_string):
    if type(list_or_string) == list:
        return repr(list_or_string)
    if type(list_or_string) == str:
        return literal_eval(list_or_string)

def return_lineup_from_db(event_id):
    party = Events.objects.filter(id=unicodetostring(event_id))
    party_values = party.values()
    source = unicodetostring(party_values[0]['source'])
    source_id = unicodetostring(party_values[0]['source_id'])
    lineup = helper.list_to_string_or_back(unicodetostring(party_values[0]['line_up']))
    print 'bron = ' , source, source_id
    return lineup

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


def db_return_query_object_by_id(event_query):
    return Events.objects.filter(id=event_query)
