CREATE TABLE User (
    id TEXT AS UUID PRIMARY KEY,
    username TEXT,
    role TEXT,
    email TEXT,
    preferences LIST<TEXT>,
    password TEXT
);

CREATE TABLE Event (
    id TEXT AS UUID PRIMARY KEY,
    date timestamp,
    venue TEXT AS UUID
);

CREATE TABLE Venue (
    id STRING AS UUID PRIMARY KEY,
    location TEXT
);
