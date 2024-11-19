from django.contrib import admin
from django.urls import path

from user.views import UserView, ValidateUserView, JoinEventView
from event.views import EventView, EventsForUserView, EventsFromUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<uuid:user_id>/', UserView.as_view()),
    path('user/', UserView.as_view()),
    path('join/<uuid:user_id>/', JoinEventView.as_view()),
    path('join/', JoinEventView.as_view()),
    path('validate/', ValidateUserView.as_view()),
    path('event/<int:page>/', EventView.as_view()),
    path('event/', EventView.as_view()),
    path('eventsforuser/<uuid:user_id>/', EventsForUserView.as_view()),
    path('eventsfromuser/<uuid:user_id>/', EventsFromUserView.as_view()),
]
