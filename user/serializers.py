from rest_framework import serializers

from .models import User

def serialize_user(user: User):
    serialized_user = UserSerializer(user).data

    return {
        **serialized_user,
        'joined_events': [str(event.id) for event in user.joined_events.all()],
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
