from django import forms

class NameForm(forms.Form):
    lineup = forms.CharField(label='Lineup', max_length=200)
