import pgPromise from 'pg-promise';

const pgp = pgPromise({});

export const db = pgp({
    host: process.env.DB_SERVER!,
    port: Number(process.env.DB_PORT!),
    database: process.env.DB_DATABASE!,
    user: process.env.DB_USER!,
    password: process.env.DB_PASSWORD!,
    ssl: true,
});
