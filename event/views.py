from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer

from .models import Event
from .forms import EventCreationForm
from .serializers import serialize_event

class SpecificEventView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'message': f'Event does not exist with id {event_id}'}, status=404)
        
        return Response({'data': serialize_event(event)}, status=200)

class EventView(APIView):
    def get(self, request, page):
        events = Event.objects.all()[page:(page + 200)]

        serialized_events = []

        for event in events:
            serialized_events.append(serialize_event(event))

        return Response({'data': serialized_events}, status=200)
    
    def post(self, request):
        if request.data.get('tags') is None:
            return Response({'message': 'Invalid request'}, status=400)

        form = EventCreationForm({
            **request.data,
            'tags': ''
        })

        if not form.is_valid():
            return Response({'message': 'Invalid request data'}, status=400)

        form_data = form.cleaned_data

        organizer_id = form_data.get('organizer')

        try:
            organizer = User.objects.get(id=organizer_id)
        except User.DoesNotExist:
            return Response({'message': f'User does not exist with id {organizer_id}'}, status=404)

        event = Event.objects.create(
            organizer=organizer,
            name=form_data.get('name'),
            start_date=form_data.get('start_date'),
            end_date=form_data.get('end_date'),
            price=form_data.get('price'),
            location=form_data.get('location'),
            description=form_data.get('description'),
            cover_uri=form_data.get('cover_uri'),
            tags=request.data.get('tags'),
        )

        return Response({'data': serialize_event(event)}, status=200)

class EventsFromUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': f'User not found with id {user_id}'}, status=404)
        
        events = Event.objects.filter(organizer=user)
        serialized_events = []

        for event in events:
            serialized = serialize_event(event)

            serialized_events.append(serialized)

        return Response({'data': serialized_events}, status=200)

class EventsForUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': f'User not found with id {user_id}'}, status=404)
        
        user_preferences = user.preferences
        events = Event.objects.all()
        event_count = 0

        serialized_events = []

        for event in events:
            if event_count >= 5:
                break

            event_tags = event.tags

            for preference in user_preferences:
                if preference in event_tags:
                    event_count += 1

                    serialized_events.append(serialize_event(event))

        return Response({'data': serialized_events}, status=200)

class ParticipantsView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'message': f'Event does not exist with id {event_id}'}, status=404)
        
        participants = event.participants.all()
        serialized_participants = []

        for participant in participants:
            serialized_participants.append(UserSerializer(participant).data)

        return Response({'data': serialized_participants}, status=200)
    