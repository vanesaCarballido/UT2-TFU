from fastapi import Header, HTTPException

# Credenciales de autenticación
USERNAME = "admin"
PASSWORD = "1234"

# Táctica: Autenticación
def authenticate(
    username: str | None = Header(default=None),
    password: str | None = Header(default=None)
):

    if username != USERNAME or password != PASSWORD:

        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    return username