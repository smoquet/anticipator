from form.models import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import NameForm, DatabaseLookupForm
from vpg import *
from pf_api import pf_api

from datetime import datetime

import os
import random
import string
import unicodedata
import helper
# import vpg.filemanager
# import vpg.spotify
# import vpg.main
# from filemanager import *
# from spotify import *


def unicodetostring(unicode):
    string_out = unicodedata.normalize('NFKD', unicode).encode('ascii','ignore')
    return string_out

def index(request):
    print 'index entered'
    '''
    asks user for event_query search and looks up the results in the DB
    if no result, then look in Partyflock and store results in db, then look again

    '''


    if request.method == 'POST':
        print 'search POST entered'
        # create the searchform instance and populate it with data from the request:
        form = DatabaseLookupForm(request.POST)
        if form.is_valid():
            print 'form is valid'
            # assign the form input to the variable event_query
            event_query_unicode = form.cleaned_data['event_query']
            event_query = unicodedata.normalize('NFKD', event_query_unicode).encode('ascii','ignore')
            # search for the query in the db
            print 'query = ' , event_query

            search_result_key_value_pairs = helper.db_event_search(event_query)
            print 'search_result_key_value_pairs = ', search_result_key_value_pairs

            '''
             Partyflock lookup: if there are no results in our db, search partyflock and save result in db
            '''

            if len(search_result_key_value_pairs) == 0:
                partyflock_number_of_results = 5

                pf_events = pf_api.eventsearch(event_query, partyflock_number_of_results)

                # print pf_api.eventsearch('frenchcore', 1)
                # pf_api.lineupsearch(4653845638475)
                # print pf_api.testfunct()
                print 'pf_events = ', pf_events

                for x in range(min([partyflock_number_of_results, len(pf_events)])):
                    stamp = pf_events[x]['stamp']
                    date = datetime.fromtimestamp(stamp).strftime('%Y/%m/%d').replace('/', '-')
                    source_id = pf_events[x]['id']
                    name = unicodedata.normalize('NFKD', pf_events[x]['name']).encode('ascii','ignore').lower()
                    source = 'partyflock'
                    eventinstance = Events(name=name, date=date, source_id=source_id, source=source )
                    eventinstance.save()

                # then return the result from the db again
                print 'query = ' , event_query

            search_result_key_value_pairs = helper.db_event_search(event_query)
            print 'search_result_key_value_pairs PF if = ', search_result_key_value_pairs
            # assign search.html in template variable
            template = loader.get_template('form/results.html')
            # fill in context



            search_result_key_value_pairs
            print 'search_result_key_value_pairs', search_result_key_value_pairs
            context = { 'event_query':event_query, 'search_result_key_value_pairs':search_result_key_value_pairs}

            form = DatabaseLookupForm()

            context =   {'form': form, 'event_query':event_query, 'search_result_key_value_pairs':search_result_key_value_pairs}
            return HttpResponse(template.render(context, request))

    # if the form is not filled in is thus GET
    form = DatabaseLookupForm()
    return render(request, 'form/index.html', {'form': form})



def result(request):
    '''
    This function gets the event name, should get id
    and asks for some variable inputs: top_x_tracks, playlist name, etc
    then gives this to the exit view
    also saves the line_up of the selected event in db
    '''
    print 'result request = ' , request.POST


    # accept the request
    query_object = request.POST
    print 'query_object = ', query_object
    # parse it
    event_id = query_object.__getitem__('id')

    ''' Saves the lineup of chosen event in db '''
    # saves the corresponding line_up in db
    party = Events.objects.filter(id=unicodetostring(event_id))
    party_values = party.values()
    source_id = unicodetostring(party_values[0]['source_id'])
    # get lineup;
    lineup = pf_api.lineupsearch(str(source_id))
    # print 'result view lineup = ', lineup
    # save line_up to corresponding event
    local_event_instance = helper.db_return_query_object_by_id(event_id)
    local_event_instance.update(line_up=helper.list_to_string_or_back(lineup))
    print 'event lineup saved in exit view'


    # get event name form id
    event_name = helper.db_search_by_id(event_id)['name']
    print 'parsed event_id =  ', event_id

    # ask for more input in the form and give it an initial value to pass on the event name
    form = NameForm(initial={'event_id': event_id, 'playlist_name':event_name })
    # and pass it all to exit

    # 1e return poging, faalde
    # context =   {'event_id': event_id}
    # return render(request, 'form/result.html', {'form': form})

    #2e return poging lukt
    template = loader.get_template('form/result.html')
    context =   {'form': form}
    return HttpResponse(template.render(context, request))


def victory(request):
    '''
    this gets the post request from the NameForm in result view and processes the results
    this is where the magic happens
    '''
    print 'exit request = ', request.POST

    '''
    create or get session
    '''
    sid = request.session._get_or_create_session_key()
    print 'session id  = ', sid
    # sid = '123'
    top_x_tracks, client_id, client_secret, redirect_uri = main.initialise()
    spot_token, username = main.init_spot(redirect_uri, client_id, client_secret, sid)


    '''
    parse form
    '''
    print 'form data = ', request.session.get('form_data')
    # create a form instance and populate it with data from the request: to be able to parse the input
    form = NameForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        playlist_name = form.cleaned_data['playlist_name']
        public = form.cleaned_data['public']
        top_x_tracks = form.cleaned_data['top_x_tracks']
        event_id = form.cleaned_data['event_id']

        print 'type(event_id) = ', type(event_id)

        '''
        if line_up is already there
        partyflock will give us line up here
        '''

	# get source (partyflock) and source_id

        party = Events.objects.filter(id=unicodetostring(event_id))
        party_values = party.values()
        source = unicodetostring(party_values[0]['source'])
        source_id = unicodetostring(party_values[0]['source_id'])
        lineup = helper.list_to_string_or_back(unicodetostring(party_values[0]['line_up']))
        print 'lineup type', type(lineup)
        print 'bron = ' , source, source_id


        #  'save submitted data in session'
        for k, v in form.cleaned_data.iteritems():
            request.session[k] = v

        # if spot token[0] is false (see spotify file get_token function) then there is no token in cache
        if not spot_token[0]:

            # submitted_data = ['playlist_name','public','top_x_tracks','event_id']
            # map(save_in_session, submitted_data)

            print 'no spot token and thus redirect to spot and then back to callspot'
            # and therefore user needs to be redirected to spot_token[1], wich is the auth_url
            #when user comes back from that he will arrive at our redirect_uri, wich is callspot
            return redirect(spot_token[1])

    else:
        try:
            # attempt to load saved data from session
            playlist_name = request.session['playlist_name']
            public = request.session['public']
            top_x_tracks = request.session['top_x_tracks']
            event_id = request.session['event_id']
        except KeyError:
            print 'geen posted form en geen session :/'
            return redirect(index)


    party = Events.objects.filter(id=unicodetostring(event_id))
    party_values = party.values()
    source = unicodetostring(party_values[0]['source'])
    source_id = unicodetostring(party_values[0]['source_id'])
    print 'bron = ' , source, source_id

    lineup = helper.list_to_string_or_back(unicodetostring(party_values[0]['line_up']))

    '''
    Spotify happens below
    - search for artists
    - get the top tracks
    - do the magic you know
    '''
    artist_ids = spotify.artist_id_list_gen(lineup, spot_token[1])

    # handles the exception when there isnt a single result from artist searches in spotify
    if artist_ids != []:
        track_id_list = spotify.tracklist_gen(artist_ids, top_x_tracks, spot_token[1])
        spotify.write_playlist(track_id_list, playlist_name, spot_token[1], username)

    '''
    Give context to HTML to print to browser
    '''

    template = loader.get_template('form/victory.html')


    context = {
        # 'lineup': lineup,
        'playlist_name': playlist_name,
        'username':username,
        'public':public,
        'top_x_tracks':top_x_tracks,
        'event_id': event_id,
        'lineup': lineup,
        'victory_or_defeat': 'victory'
    }

    if artist_ids == []:
        context['victory_or_defeat'] = 'defeat'

    return HttpResponse(template.render(context, request))


def callspot(request):
    print 'callspot entered'

    sid = request.session._get_or_create_session_key()
    top_x_tracks, client_id, client_secret, redirect_uri = main.initialise()

    # the build_absolute_uri method from class HttpRequest retrieves the string given by spotify to user
    # while redrecting back to us, this is stored in spot_response
    spot_response = HttpRequest.build_absolute_uri(request)
    # gets user with a token and caches it in the server
    spot_token = spotify.make_token(spot_response, sid, client_id, client_secret, redirect_uri)

    return redirect(exit)

def vpgtest(request):
    sid = request.session._get_or_create_session_key()
    # read settings
    lineup, top_x_tracks, playlist_name, spot_token = main.initialise()
    # if spot token[0] is false (see spotify file get_token function) then there is no token in chache
    if type(spot_token) != dict:
        if not spot_token[0]:
            # and therefore user needs to be redirected to spot_token[1], wich is the auth_url
            return redirect(spot_token[1])
    artist_ids = spotify.artist_id_list_gen(lineup, spot_token)
    track_id_list = spotify.tracklist_gen(artist_ids, top_x_tracks, spot_token)
    template = loader.get_template('form/result.html')
    context = {
        'lineup': track_id_list
    }
    return HttpResponse(template.render(context, request))
