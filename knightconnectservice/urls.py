from django.contrib import admin
from django.urls import path

from user.views import (
    UserView,
    ValidateUserView,
    JoinEventView,
    EditUserView,
    FriendsView,
    FriendRequestView,
    RejectFriend,
)

from event.views import (
    EventView,
    EventsForUserView,
    EventsFromUserView,
    SpecificEventView,
    ParticipantsView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<uuid:user_id>/', UserView.as_view()),
    path('user/', UserView.as_view()),

    path('friends/<uuid:user_id>/', FriendsView.as_view()),
    path('friends/', FriendsView.as_view()),
    path('friendrequest/<uuid:user_id>/', FriendRequestView.as_view()),
    path('friendrequest/', FriendRequestView.as_view()),
    path('rejectfriend/', RejectFriend.as_view()),

    path('edituser/', EditUserView.as_view()),
    path('join/<uuid:user_id>/', JoinEventView.as_view()),
    path('join/', JoinEventView.as_view()),
    path('validate/', ValidateUserView.as_view()),
    path('getevent/<uuid:event_id>/', SpecificEventView.as_view()),
    path('event/<int:page>/', EventView.as_view()),
    path('event/', EventView.as_view()),
    path('eventsforuser/<uuid:user_id>/', EventsForUserView.as_view()),
    path('eventsfromuser/<uuid:user_id>/', EventsFromUserView.as_view()),

    path('participants/<uuid:event_id>/', ParticipantsView.as_view()),
]
