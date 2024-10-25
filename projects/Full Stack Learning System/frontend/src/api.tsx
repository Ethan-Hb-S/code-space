import axios from 'axios';
import config from '../config.json';

export const api = axios.create({
    baseURL: `http://127.0.0.1:${config.BACKEND_PORT}`,
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
});