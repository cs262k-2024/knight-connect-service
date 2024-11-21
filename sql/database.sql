DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS event_user;
DROP TABLE IF EXISTS event;

CREATE TABLE user (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(), -- UUID for unique identification
    name VARCHAR(100) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL, -- Email field ensures uniqueness
    preferences TEXT[] NOT NULL, -- PostgreSQL array field for preferences
    password VARCHAR(255) NOT NULL,
    bio TEXT NOT NULL
);

CREATE TABLE event_user (
    id SERIAL PRIMARY KEY, -- Optional: Auto-incrementing primary key for the relationship table
    user_id UUID NOT NULL, -- References the User table
    event_id UUID NOT NULL, -- References the Event table
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    CONSTRAINT fk_event FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
    UNIQUE (user_id, event_id) -- Ensures unique relationships between a user and an event
);

CREATE TABLE event (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(), -- UUID generation depends on the database being used
    organizer_id UUID NOT NULL, -- References the User model
    name VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    price FLOAT,
    location VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    cover_uri TEXT,
    tags TEXT[] NOT NULL, -- PostgreSQL array field
    CONSTRAINT fk_organizer FOREIGN KEY (organizer_id) REFERENCES user(id) ON DELETE CASCADE
);
