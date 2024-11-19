from rest_framework import serializers

from .models import Event

def serialize_event(event: Event):
    serialized_event = EventSerializer(event).data

    return {
        **serialized_event,
        'organizer': str(serialized_event['organizer'])
    }

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        