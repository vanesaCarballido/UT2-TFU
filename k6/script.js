import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';


export const options = {
    vus: 1,
    iterations: 10,
};


export default function () {

    const response = http.get(
        'http://localhost:8000/saludo'
    );

    check(response, {
        'respuesta exitosa': (r) => r.status === 200,
    });

    console.log(
        `Status: ${response.status}`
    );

    sleep(1);
}

