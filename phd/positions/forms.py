from django import forms

class AddPositionForm(forms.Form):
    position_pk = forms.CharField(widget=forms.HiddenInput())