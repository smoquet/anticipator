from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import NameForm
from vpg import *
# import vpg.filemanager
# import vpg.spotify
# import vpg.main
# from filemanager import *
# from spotify import *

def index(request):
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
            template = loader.get_template('form/result.html')
            context = {
                'lineup': lineup
            }
            return HttpResponse(template.render(context, request))
            # return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'form/index.html', {'form': form})

def vpgtest(request):
    #hard coded vars for testing:
    lineup, top_x_tracks, playlist_name, spot_token, username = main.initialise('args')
    # if spot token[0] is false (see spotify file get_token function) then there is no token in chache
    if not spot_token[0]:
        # and therefore user needs to be redirected to spot_token[1], wich is the auth_url
        #when user comes back from that he will arrive at our redirect_uri, wich is callspot
        return redirect(spot_token[1])
    # puts html file in template
    template = loader.get_template('form/result.html')
    # this key valuea pair is called upon in the html file
    context = {
        'lineup': lineup
    }
    return HttpResponse(template.render(context, request))

def callspot(request):
    # a user without cache_token arrives from oauth, wich was given to him in vpgtest
    # in request wich is an object, wich comes from the browers, we find the spotify responseURL and
    # lots of ohter info, like request type (post, get, etc) and other shite
    lineup, top_x_tracks, playlist_name, spot_token, username = main.initialise('args')
    settings_file = 'vpg/voorpretgen.ini'
    # the build_absolute_uri method from class HttpRequest retrieves the stri ng given by spotify to user
    # while redrecting back to us, this is stored in spot_response
    spot_response = HttpRequest.build_absolute_uri(request)
    # read settings
    top_x_set, client_id, client_secret, redirect_uri = filemanager.read_settings(settings_file)
    #make_token
    spot_token = spotify.make_token(spot_response, 'milowinterburn', client_id, client_secret, redirect_uri)
    #make artist ids
    artist_ids = spotify.artist_id_list_gen(lineup, spot_token)
    # get tracks
    track_id_list = spotify.tracklist_gen(artist_ids, top_x_tracks, spot_token)
    # spotify.write_playlist(track_id_list, playlist_name, spot_token, username)

    template = loader.get_template('form/result.html')
    context = {
        'lineup': track_id_list
    }
    return HttpResponse(template.render(context, request))
