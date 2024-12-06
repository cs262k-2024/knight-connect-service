# KnightConnect Web Service

This is the data service application for the [KnightConnect](https://github.com/cs262k-2024/knight-connect-project) App

- https://knightconnect-aqe5cmfkaqgca7bw.canadacentral-01.azurewebsites.net

# Local Setup
- `pip install -r requiremnts.txt`
- `python manage.py migrate`
- `python manage.py runserver`

# Read data route URLs:
- `user/<uuid:user_id>/`
- `join/<uuid:user_id>/`
- `validate/`
- `getevent/<uuid:event_id>/`
- `event/<int:page>/`
- `eventsforuser/<uuid:user_id>/`
- `eventsfromuser/<uuid:user_id>/`
