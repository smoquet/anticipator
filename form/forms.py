from django import forms


# creer hier het formulier, dat instantiated wordt in views.py
# daarna in index.html gestopt
class NameForm(forms.Form):
    lineup = forms.CharField(label='Lineup', max_length=200, widget=forms.TextInput(attrs={'class': 'charfield'}))
    playlist_name = forms.CharField(label='Playlist Name', max_length=200, widget=forms.TextInput(attrs={'class': 'charfield'}))
    topX = forms.CharField(label= 'Number of tracks per artist', max_length=1, widget=forms.NumberInput(attrs={'class': 'intfield'}))
    sort = forms.BooleanField(label='Sort', required = False, initial = True, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
    public = forms.BooleanField(label='Public playlist', required=False, initial = True, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
