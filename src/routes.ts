import { Request, Response } from 'express';

import { db } from './crud';

export function helloWorld(req: Request, res: Response) {
    res.send('Hello, world!');
}

function returnDataOr404(res: Response, data: any) {
    if (data === null) {
        res.sendStatus(404);
    } else {
        res.send(data);
    }
}

export async function readEvents(req: Request, res: Response, next: Function) {
    try {
        const data = await db.many('SELECT * FROM Event');
        returnDataOr404(res, data);
    } catch (err) {
        next(err);
    }
}
