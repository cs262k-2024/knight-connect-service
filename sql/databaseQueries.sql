-- GET Request: Retrieve a specific event by event_id
SELECT * 
FROM event 
WHERE id = '<event_id>';

-- GET Request: Retrieve events in paginated format
SELECT * 
FROM event
ORDER BY date_created DESC
LIMIT 15 OFFSET <page * 15>;

-- Create new event
SELECT * 
FROM user
WHERE id = '<organizer_id>';

INSERT INTO event (
    id, organizer_id, name, start_date, end_date, price, location, description, cover_uri, tags, date_created
) VALUES (
    gen_random_uuid(), '<organizer_id>', '<name>', '<start_date>', '<end_date>', <price>, '<location>', '<description>', '<cover_uri>', ARRAY['<tag1>', '<tag2>', ...], NOW()
)
RETURNING *;

-- GET Request: Retrieve events organized by a specific user
SELECT * 
FROM event
WHERE organizer_id = '<user_id>'
ORDER BY start_date DESC;

-- Events from user preferences
SELECT * 
FROM user
WHERE id = '<user_id>';

SELECT * 
FROM event
WHERE tags && ARRAY[<user_preferences>] -- Array overlap operator for PostgreSQL
LIMIT 5;

-- USERS

-- Get user
SELECT * 
FROM user 
WHERE id = '<user_id>';

-- Create user
INSERT INTO user (
    id, name, email, password, bio, preferences
) VALUES (
    gen_random_uuid(), '<name>', '<email>', '<hashed_password>', '<bio>', ARRAY['<preference1>', '<preference2>', ...]
)
RETURNING *;

-- Add user to event
SELECT * 
FROM user 
WHERE id = '<user_id>';

SELECT * 
FROM event 
WHERE id = '<event_id>';

INSERT INTO event_user (user_id, event_id)
VALUES ('<user_id>', '<event_id>')
ON CONFLICT DO NOTHING; -- Prevent duplicates

-- Get user joined events
SELECT e.* 
FROM event e
JOIN event_user eu ON e.id = eu.event_id
WHERE eu.user_id = '<user_id>';

-- Validate user
SELECT * 
FROM user 
WHERE email = '<email>';

SELECT * 
FROM user 
WHERE email = '<email>' AND password = '<hashed_password>';

-- Edit user profile
SELECT * 
FROM user 
WHERE id = '<user_id>';

UPDATE user
SET 
    name = COALESCE('<name>', name),
    email = COALESCE('<email>', email),
    preferences = COALESCE(ARRAY['<preference1>', '<preference2>', ...], preferences),
    password = COALESCE('<hashed_password>', password),
    bio = COALESCE('<bio>', bio)
WHERE id = '<user_id>'
RETURNING *;
