import { Request, Response } from 'express';

export function helloWorld(req: Request, res: Response) {
    res.send('Hello, world!');
}
