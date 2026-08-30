import uvicorn
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="TFU UT2 Service B")

# Probabilidad de que Service B esté disponible
availability_probability = 1.0

class ConfigRequest(BaseModel):
    prob: float


@app.get("/saludo")
def saludo():

    # Simula una falla temporal
    if random.random() > availability_probability:
        raise HTTPException(
            status_code=503,
            detail="Service B temporalmente no disponible"
        )

    return {
        "mensaje": "Hola desde Service B"
    }


@app.post("/config")
def configurar(config: ConfigRequest):

    global availability_probability

    if not 0 <= config.prob <= 1:
        raise HTTPException(
            status_code=400,
            detail="La probabilidad debe estar entre 0 y 1"
        )

    availability_probability = config.prob

    return {
        "availability_probability": availability_probability
    }


if __name__ == "__main__":
    uvicorn.run(
        "service_b.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )

