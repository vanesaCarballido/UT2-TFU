import uvicorn

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

from service_a.config import (
    SERVICE_B_URL,
    SERVICE_B_REPLICA_URL
)

from service_a.utils import (
    log_event,
    retry_request,
    request_with_replication
)



from service_a.auth import authenticate
from service_a.rate_limit import check_rate_limit


app = FastAPI(title="TFU UT2 API Service A")

# Datos base de productos

products = [
    {
        "id": 1,
        "name": "Jugo de naranja",
        "price": 100
    },
    {
        "id": 2,
        "name": "Galletas de chocolate",
        "price": 130
    },
    {
        "id": 3,
        "name": "Jugo de manzana",
        "price": 100
    },
    {
        "id": 4,
        "name": "Tostadas",
        "price": 30
    },
]


class Product(BaseModel):
    name: str
    price: float


# Endpoints de productos con autenticación y límite de acceso

@app.get("/products")
def get_products(
    username: str = Header(None),
    password: str = Header(None)
):
    # Autenticación
    authenticate(username, password)

    # Límite de acceso
    check_rate_limit(username)

    return products


@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    username: str = Header(None),
    password: str = Header(None)
):
    authenticate(username, password)
    check_rate_limit(username)

    for product in products:

        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail=f"No se ha encontrado el producto de id: {product_id}"
    )


@app.post("/products")
def create_product(
    product: Product,
    username: str = Header(None),
    password: str = Header(None)
):
    authenticate(username, password)
    check_rate_limit(username)

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return new_product


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product: Product,
    username: str = Header(None),
    password: str = Header(None)
):
    authenticate(username, password)
    check_rate_limit(username)

    for existing_product in products:

        if existing_product["id"] == product_id:

            existing_product["name"] = product.name
            existing_product["price"] = product.price

            return existing_product

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    username: str = Header(None),
    password: str = Header(None)
):
    authenticate(username, password)
    check_rate_limit(username)

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            return {
                "message": "Producto eliminado"
            }

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )

# Endpoint de saludo para probar reintentos y replicación
@app.get("/saludo")
def saludo():

    # Primero se intenta acceder a B1
    # realizando hasta 3 intentos.
    try:

        return retry_request(
            f"{SERVICE_B_URL}/saludo"
        )

    except Exception as e:

        log_event(
            f"B1 unavailable after retries: {e}"
        )

        # Si B1 continúa fallando,
        # se utiliza la instancia replicada B2.
        return request_with_replication([
            f"{SERVICE_B_REPLICA_URL}/saludo"
        ])


if __name__ == "__main__":

    uvicorn.run(
        "service_a.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
