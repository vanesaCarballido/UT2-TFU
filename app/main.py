from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="TFU UT2 API")

#Datos para la abse de datos: 
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


# Obtener todos los productos de la base
@app.get("/products")
def get_products():
    return products


# Obtener un producto de la base por el id
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="No se ha encontrado el producto de id: {product_id}"
    )

#Agregar productos a la base
@app.post("/products")
def create_product(product: Product):

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return new_product

# Actualizar productos en la base
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):

    for existing_product in products:

        if existing_product["id"] == product_id:

            existing_product["name"] = product.name
            existing_product["price"] = product.price

            return existing_product

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )

#Borrar productos de la base
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

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