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
    lineup, top_x_tracks, playlist_name, spot_token, username = main.initialise('args')
    if not spot_token[0]:
        return redirect(spot_token[1])
    template = loader.get_template('form/result.html')
    context = {
        'lineup': lineup
    }
    return HttpResponse(template.render(context, request))

def callspot(request):
    lineup, top_x_tracks, playlist_name, spot_token, username = main.initialise('args')
    settings_file = 'vpg/voorpretgen.ini'
    spot_response = HttpRequest.build_absolute_uri(request)
    top_x_set, client_id, client_secret, redirect_uri = filemanager.read_settings(settings_file)
    spot_token = spotify.make_token(spot_response, 'henk', client_id, client_secret, redirect_uri)
    artist_ids = spotify.artist_id_list_gen(lineup, spot_token)

    template = loader.get_template('form/result.html')
    context = {
        'lineup': artist_ids
    }
    return HttpResponse(template.render(context, request))
