SELECT * FROM User;

SELECT * FROM Event
WHERE start > '2024-01-01 00:00:00';

SELECT User.id, User.username, User.email
FROM User
JOIN UserEvent ON User.id = UserEvent.userID
WHERE UserEvent.eventID = '1234';

SELECT * FROM Event
WHERE eventtype = 'concert';

SELECT COUNT(eventID) AS event_count
FROM UserEvent
WHERE userID = '5678';

SELECT Event.title, Event.start, User.username
FROM Event
JOIN UserEvent ON Event.id = UserEvent.eventID
JOIN User ON UserEvent.userID = User.id
ORDER BY Event.start;

SELECT * FROM User
WHERE role = 'admin';

SELECT * FROM Event
WHERE description ILIKE '%workshop%';

UPDATE User
SET role = 'organizer'
WHERE email = 'user@example.com';

DELETE FROM User
WHERE id = '5678';

SELECT * FROM Event
ORDER BY price DESC;
