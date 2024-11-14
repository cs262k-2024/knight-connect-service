DROP TABLE IF EXISTS AccountEvent;
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Event;

CREATE TABLE Account (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    email TEXT NOT NULL,
    preferences TEXT[],
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

CREATE TABLE AccountEvent (
    accountID UUID REFERENCES Account(id),
    eventID UUID REFERENCES Event(id)
);

