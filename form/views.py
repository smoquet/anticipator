from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render

from .forms import NameForm

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data to the variables
            # they are used as input to the spotify api

            lineup = form.cleaned_data['lineup']
            playlist_name = form.cleaned_data['playlist_name']
            sort = form.cleaned_data['sort']
            public = form.cleaned_data['public']

            template = loader.get_template('form/result.html')
            context = {
                'lineup': lineup, 'playlist_name': playlist_name,
                'sort':sort, 'public':public,
            }
            # redirect to a new URL:
            return HttpResponse(template.render(context, request))
            # return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'form/index.html', {'form': form})
