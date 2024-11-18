import hashlib

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from .forms import UserCreationForm, UserValidationForm

class UserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': f'User not found with id {user_id}'}, status=404)
        
        serialized_user = UserSerializer(user).data

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

        return Response({'data': UserSerializer(user).data}, status=200)

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

        return Response({'data': UserSerializer(user).data}, status=200)
