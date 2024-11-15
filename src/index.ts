import express from 'express';
import dotenv from 'dotenv';

import * as Routes from './routes';

dotenv.config();

const app = express();
const port = process.env.PORT || 8000;
const router = express.Router();

router.use(express.json());

router.get('/', Routes.helloWorld);
router.get('/events', Routes.readEvents);

app.use(router);
app.listen(port, () => console.log(`Listening on port ${port}`));
