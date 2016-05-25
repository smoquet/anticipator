from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import NameForm
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

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            lineup = form.cleaned_data['lineup']
            playlist_name = form.cleaned_data['playlist_name']
            sort = form.cleaned_data['sort']
            public = form.cleaned_data['public']
            template = loader.get_template('form/result.html')

            # process the data
            artist_ids = spotify.artist_id_list_gen(lineup, spot_token[1])
            track_id_list = spotify.tracklist_gen(artist_ids, top_x_tracks, spot_token[1])
            spotify.write_playlist(track_id_list, playlist_name, spot_token[1], username)


            # SUCCES render the it's all good result.html
            template = loader.get_template('form/result.html')
            # these key value pairs are called upon in the html file
            context = {
                'lineup': lineup,
                'playlist_name': playlist_name,
                'username':username,
                'sort':sort,
                'public':public,
                'top_x_tracks':top_x_tracks,
            }

            return HttpResponse(template.render(context, request))
            # return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'form/index.html', {'form': form})


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
