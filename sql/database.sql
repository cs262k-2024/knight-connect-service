CREATE TABLE User (
    id TEXT AS UUID PRIMARY KEY,
    username TEXT NOT NULL,
    role TEXT,
    email TEXT NOT NULL,
    preferences LIST<TEXT>,
    passwordhash TEXT NOT NULL,
    bio TEXT
);

CREATE TABLE Event (
    id TEXT AS UUID PRIMARY KEY,
    title TEXT NOT NULL,
    time TIMESTAMP NOT NULL,
    price TEXT,
    location TEXT,
    description TEXT,
    pictureurl TEXT,
    eventtype TEXT
);

CREATE TABLE UserEvent (
    userID TEXT AS UUID REFERENCES User(id),
    eventID TEXT AS UUID REFERENCES Event(id)
);

