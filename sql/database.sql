DROP TABLE IF EXISTS UserEvent;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Event;

CREATE TABLE User (
    id UUID PRIMARY KEY,
    username TEXT NOT NULL,
    role TEXT,
    email TEXT NOT NULL,
    preferences LIST<TEXT>,
    passwordhash TEXT NOT NULL,
    bio TEXT
);

CREATE TABLE Event (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    time TIMESTAMP NOT NULL,
    price TEXT,
    location TEXT,
    description TEXT,
    pictureurl TEXT,
    eventtype TEXT
);

CREATE TABLE UserEvent (
    userID UUID REFERENCES User(id),
    eventID UUID REFERENCES Event(id)
);

