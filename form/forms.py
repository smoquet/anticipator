from django import forms


# creer hier het formulier, dat instantiated wordt in views.py
# daarna in index.html gestopt
class NameForm(forms.Form):
    lineup = forms.CharField(label='Lineup', max_length=200)
    playlist_name = forms.CharField(label='Playlist Name', max_length=200)
    sort = forms.BooleanField(label='Sort', required = False, initial = True )
    public = forms.BooleanField(label='Public playlist', required=False, initial = True)
