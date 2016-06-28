from django import forms

ACCEPTED_FORMATS = ['%d-%m-%Y', '%d.%m.%Y', '%d/%m/%Y']
# creer hier het formulier, dat instantiated wordt in views.py
# daarna in index.html gestopt
class NameForm(forms.Form):
    lineup = forms.CharField(label='Lineup', max_length=200)
    playlist_name = forms.CharField(label='Playlist Name', max_length=200)
    sort = forms.BooleanField(label='Sort', required = False, initial = True )
    public = forms.BooleanField(label='Public playlist', required=False, initial = True)
    top_x_tracks = forms.IntegerField(label='Number of tracks per artist', required=False , initial = 5, max_value = 10, min_value = 1)
    db_input_test_name = forms.CharField(label='db_input_test_name', max_length=200)
    db_input_test_date = forms.DateField(input_formats=ACCEPTED_FORMATS)
    db_input_test_line_up = forms.CharField(label='db_input_test_line_up')
