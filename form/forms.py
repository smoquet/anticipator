from django import forms

ACCEPTED_FORMATS = ['%d-%m-%Y', '%d.%m.%Y', '%d/%m/%Y']
# creer hier het formulier, dat instantiated wordt in views.py
# daarna in index.html gestopt
class NameForm(forms.Form):
    playlist_name = forms.CharField(label='Playlist Name', max_length=200)
    public = forms.BooleanField(label='Public playlist', required=False, initial = True)
    top_x_tracks = forms.IntegerField(label='Number of tracks per artist', required=False , initial = 5, max_value = 10, min_value = 1)

    # lineup = forms.CharField(label='Lineup', max_length=200)
    # sort = forms.BooleanField(label='Sort', required = False, initial = True )
    # db_input_test_name = forms.CharField(label='db_input_test_name', max_length=200)
    # db_input_test_date = forms.DateField(input_formats=ACCEPTED_FORMATS)
    # db_input_test_line_up = forms.CharField(label='db_input_test_line_up')


class DatabaseLookupForm(forms.Form):
    event_query = forms.CharField(label='event_query', max_length=200)
