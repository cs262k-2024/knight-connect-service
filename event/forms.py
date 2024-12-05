from django import forms

class EventCreationForm(forms.Form):
    organizer = forms.UUIDField()

    name = forms.CharField(max_length=255)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()

    price = forms.CharField(required=False)

    location = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    tags = forms.CharField(required=False)

    cover_uri = forms.CharField(required=False)
    