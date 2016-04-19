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
