import time
from fastapi import Header, HTTPException


requests = {}

MAX_REQUESTS = 4
WINDOW = 60

# Táctica: Límite de acceso
def check_rate_limit(
    username: str | None = Header(default=None)
):

    if username is None:
        return

    current_time = time.time()

    if username not in requests:
        requests[username] = []

    # Eliminar solicitudes anteriores a un minuto
    requests[username] = [
        request_time
        for request_time in requests[username]
        if current_time - request_time < WINDOW
    ]

    if len(requests[username]) >= MAX_REQUESTS:

        raise HTTPException(
            status_code=429,
            detail="Límite de solicitudes excedido"
        )

    requests[username].append(current_time)