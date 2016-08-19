from form.models import *
import unicodedata
from ast import literal_eval
from pf_api import pf_api
from datetime import datetime

def unicodetostring(unicode):
    string_out = unicodedata.normalize('NFKD', unicode).encode('ascii','ignore')
    return string_out

def list_to_string_or_back(list_or_string):
    if type(list_or_string) == list:
        return repr(list_or_string)
    if type(list_or_string) == str:
        return literal_eval(list_or_string)

def partyflock_search_and_save(event_query, partyflock_number_of_results):
    '''
    expects a query as string, and a max number_of_results as int
    searches for event in Partyflock
    and saves result to DatabaseLookupForm
    return nothing
    '''
    pf_events = pf_api.eventsearch(event_query, partyflock_number_of_results)
    print 'pf_events = ', pf_events

    for x in range(min([partyflock_number_of_results, len(pf_events)])):
        stamp = pf_events[x]['stamp']
        date = datetime.fromtimestamp(stamp).strftime('%Y/%m/%d').replace('/', '-')
        source_id = pf_events[x]['id']
        name = unicodedata.normalize('NFKD', pf_events[x]['name']).encode('ascii','ignore').lower()
        source = 'partyflock'
        eventinstance = Events(name=name, date=date, source_id=source_id, source=source )
        eventinstance.save()

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
