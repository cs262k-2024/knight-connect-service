from rest_framework import serializers

from .models import User

def serialize_user(user: User):
    serialized_user = UserSerializer(user).data

    return {
        **serialized_user,
        'joined_events': [str(event.id) for event in user.joined_events.all()],
        'friends': [str(user.id) for user in user.friends.all()],
        'incoming_requests': [str(user.id) for user in user.incoming_requests.all()],
    }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'preferences',
            'bio',
        ]
