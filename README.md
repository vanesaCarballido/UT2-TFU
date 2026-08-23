# UT2-TFU

## Ejecución local

### Instalar requerimientos:

Para ejecutar la API en el entorno local, es necesario instalar FastAPI y Uvicorn.

**En Windows:**

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

**En macOS:**

```bash
pip3 install fastapi
pip3 install "uvicorn[standard]"
```

Una vez instalados los requerimientos, se ejecuta la aplicación con:

```bash
python -m uvicorn app.main:app --reload
```

### Ejecutar la API

Para utilizar la página de documentación interactiva que se crea mediante Swagger UI., se abre en el navegador:

`http://localhost:8000/docs`

---

## Ejecución con Docker

Para construir la imagen y ejecutar el contenedor, se utiliza:

```bash
docker compose up --build
```

Una vez iniciada la aplicación, la documentación interactiva de FastAPI estará disponible en:

`http://localhost:8000/docs`

## Fuentes

* Ander Fernández — [Cómo crear una API en Python](https://anderfernandez.com/blog/como-crear-api-en-python/)
* FastAPI — [Tutorial](https://fastapi.tiangolo.com/tutorial/)
* Docker — [Python Language-Specific Guide](https://docs.docker.com/guides/python/)
