from form.models import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import NameForm, DatabaseLookupForm
from vpg import *
import random
import string
# import vpg.filemanager
# import vpg.spotify
# import vpg.main
# from filemanager import *
# from spotify import *


def index(request):
    print 'index entered'
    '''
    asks user for event_query search and looks up the results in the DB
    if no result, then look in Partyflock and store results in db, then look again

    TODO
    add search field in POST version of index

    '''

    if request.method == 'POST':
        print 'search POST entered'
        # create the searchform instance and populate it with data from the request:
        form = DatabaseLookupForm(request.POST)
        if form.is_valid():
            print 'form is valid'
            # assign the form input to the variable event_query
            event_query = form.cleaned_data['event_query']
            # search for the query in the db
            search_results = Events.objects.filter(name=event_query)
            search_results_values = search_results.values()
            # initialise result list
            search_result_list_of_names = []
            # search_result_list_of_tracks_temp = []
            # create a list with the names of events as results
            for x in search_results_values:
                search_result_list_of_names.append(x['name'])
                # search_result_list_of_tracks_temp.append(x['line_up'])

            '''
             Partyflock lookup: if there are no results in our db, search partyflock and save result in db
            '''

            if len(search_result_list_of_names) == 0:
                partyflock_result = ['eventname', '2001-02-02', 'artist1;artist2;artist3']
                eventinstance = Events(name='eventname', date='2001-02-02', line_up='artist1;artist2;artist3' )
                eventinstance.save()
                # then return the result from the db again
                search_results = Events.objects.filter(name='eventname')
                search_results_values = search_results.values()
                # initialise result list
                search_result_list_of_names = []
                # search_result_list_of_tracks_temp = []
                # create a list with the names of events as results
                for x in search_results_values:
                    search_result_list_of_names.append(x['name'])

            # assign search.html in template variable
            template = loader.get_template('form/index.html')
            # fill in context
            context = { 'event_query':event_query, 'search_result_list':search_result_list_of_names}

            return HttpResponse(template.render(context, request))


    # if the form is not filled in is thus GET
    form = DatabaseLookupForm()
    return render(request, 'form/index.html', {'form': form})



def result(request):
    '''
    This function gets the event name, source and source_id
    and asks for some variable inputs: top_x_tracks, playlist name, etc
    then gives this to the exit view
    '''
    print 'result request = ' , request.POST

    # accept the request
    query_object = request.POST
    # parse it
    event_name = query_object.__getitem__('name')
    print 'parsed event_name =  ', event_name

    # ask for more input in the form and give it an initial value to pass on the event name
    form = NameForm(initial={'event_name': event_name})
    # and pass it all to exit

    # 1e return poging, faalde
    # context =   {'event_name': event_name}
    # return render(request, 'form/result.html', {'form': form})

    #2e return poging lukt
    template = loader.get_template('form/result.html')
    context =   {'form': form}
    return HttpResponse(template.render(context, request))


def exit(request):
    '''
    this gets the post request from the NameForm in result view and processes the results
    this is where the magic happens
    '''
    print 'exit request = ', request.POST

    '''
    create session
    '''
    # sid = request.session._get_or_create_session_key()
    sid = '123'
    lineup, top_x_tracks, playlist_name, spot_token, username = main.initialise(sid)
    # top_x_tracks, spot_token = main.initialise()
    # if spot token[0] is false (see spotify file get_token function) then there is no token in chache
    print spot_token
    if not spot_token[0]:
        print 'no spot token and thus redirect to spot and then bck to cllsport'
        # and therefore user needs to be redirected to spot_token[1], wich is the auth_url
        #when user comes back from that he will arrive at our redirect_uri, wich is callspot
        return redirect(spot_token[1])


    '''
    parse form
    '''

    # create a form instance and populate it with data from the request: to be able to parse the input
    form = NameForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        playlist_name = form.cleaned_data['playlist_name']
        public = form.cleaned_data['public']
        top_x_tracks = form.cleaned_data['top_x_tracks']
        event_name = form.cleaned_data['event_name']



        '''
        partyflock will give us line up here
        '''


        '''
        Spotify happens below
            - search for artists
            - get the top tracks
            - do the magic you know
        '''
        # this shite dont work yet
        # artist_ids = spotify.artist_id_list_gen(lineup, spot_token[1])
        # track_id_list = spotify.tracklist_gen(artist_ids, top_x_tracks, spot_token[1])
        # spotify.write_playlist(track_id_list, playlist_name, spot_token[1], username)


        '''
        Give context to HTML to print to browser
        '''

        context = {
            'lineup': lineup,
            'playlist_name': playlist_name,
            'username':username,
            'public':public,
            'top_x_tracks':top_x_tracks,
            'event_name': event_name
        }

        # return HttpResponse(template.render(context, request))
        return render(request, 'form/exit.html')


def callspot(request):
    print 'callspot entered'
    settings_file = 'vpg/voorpretgen.ini'
    top_x_set, client_id, client_secret, redirect_uri = filemanager.read_settings(settings_file)

    # gets user with a token and caches it in the server
    spot_response = HttpRequest.build_absolute_uri(request)
    # sid = request.session._get_or_create_session_key()
    sid = '123'
    spot_token = spotify.make_token(spot_response, sid, client_id, client_secret, redirect_uri)

    return redirect(index)

    # a user without cache_token arrives from oauth, wich was given to him in vpgtest
    # in request wich is an object, wich comes from the browers, we find the spotify responseURL and
    # lots of ohter info, like request type (post, get, etc) and other shite

    # lineup, top_x_tracks, playlist_name, spot_token, username = main.initialise()
    # settings_file = 'vpg/voorpretgen.ini'

    # the build_absolute_uri method from class HttpRequest retrieves the stri ng given by spotify to user
    # while redrecting back to us, this is stored in spot_response
    # spot_response = HttpRequest.build_absolute_uri(request)

    # # read settings
    # top_x_set, client_id, client_secret, redirect_uri = filemanager.read_settings(settings_file)
    # spot_token = spotify.make_token(spot_response, 'milowinterburn', client_id, client_secret, redirect_uri)
    # #make_token

    # saev in cache


    #
    # template = loader.get_template('form/result.html')
    # context = {
    #     'lineup': track_id_list
    # }
    # return HttpResponse(template.render(context, request))

def vpgtest(request):
    sid = request.session._get_or_create_session_key()
    #hard coded vars for testing:
    lineup, top_x_tracks, playlist_name, spot_token = main.initialise(sid)
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
