import hashlib

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import serialize_user
from .forms import UserCreationForm, UserValidationForm

from event.models import Event
from event.serializers import serialize_event

class UserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': f'User not found with id {user_id}'}, status=404)
        
        serialized_user = serialize_user(user)

        return Response({'data': serialized_user}, status=200)
    
    def post(self, request):
        form = UserCreationForm({
            **request.data,
            'preferences': ''
        })

        if not form.is_valid():
            return Response({'message': 'Invalid request data'}, status=400)
        
        form_data = form.cleaned_data

        name = form_data.get('name')
        email = form_data.get('email')
        password = form_data.get('password')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        bio = form_data.get('bio')
        preferences = request.data.get('preferences')

        user = User.objects.create(
            name=name,
            email=email,
            password=hashed_password,
            bio=bio,
            preferences=preferences
        )

        return Response({'data': serialize_user(user)}, status=200)

class JoinEventView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')

        if not user_id or not event_id:
            return Response({'message': 'Invalid request data'}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': f'User not found with id {user_id}'}, status=404)

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'message': f'Event not found with id {event_id}'}, status=404)

        user.joined_events.add(event)

        return Response({'data': serialize_user(user)}, status=200)
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': f'User not found with id {user_id}'}, status=404)
        
        events = user.joined_events.all()
        serialized_events = []

        for event in events:
            serialized = serialize_event(event)

            serialized_events.append(serialized)

        return Response({'data': serialized_events}, status=200)

class ValidateUserView(APIView):
    def post(self, request):
        form = UserValidationForm(request.data)
        
        if not form.is_valid():
            return Response({'message': 'Invalid request data'}, status=400)

        form_data = form.cleaned_data

        email = form_data.get('email')
        password = form_data.get('password')

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': f'User does not exist with email {email}'}, status=404)

        if user.password != hashed_password:
            return Response({'message': 'Incorrect password'}, status=400)

        return Response({'data': serialize_user(user)}, status=200)

class EditUserView(APIView):
    def post(self, request):
        data = request.data
        user_id = data['user_id']

        if not user_id:
            return Response({'message': 'Invalid request data'}, status=400)

        user = User.objects.get(id=user_id)

        if name := data.get('name'):
            user.name = name
        if email := data.get('email'):
            user.email = email
        if preferences := data.get('preferences'):
            user.preferences = preferences
        if password := data.get('password'):
            user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if bio := data.get('bio'):
            user.bio = bio

        user.save()
        serialized_user = serialize_user(user)

        return Response({'data': serialized_user}, status=200)
    