from django import forms

class EventCreationForm(forms.Form):
    organizer = forms.UUIDField()

    name = forms.CharField(max_length=255)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    price = forms.FloatField()

    location = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    tags = forms.CharField(max_length=255)

    cover_uri = forms.CharField()
    