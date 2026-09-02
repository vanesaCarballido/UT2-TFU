# UT2-TFU

## Ejecución local

### Crear el entorno virtual
**En Windows:**

```bash
python -m venv venv
```
**En macOS:**
```bash
python3 -m venv venv
```
### Activar el entorno virtual

**En Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**En macOS:**

```bash
source venv/bin/activate
```

### Instalar los requerimientos

**En Windows:**

```powershell
pip install -r requirements.txt
```

**En macOS:**

```bash
pip3 install -r requirements.txt
```

### Ejecutar los servicios

La aplicación está compuesta por un **Service A**, que funciona como API principal, y dos instancias replicadas del **Service B**:

```text
Service A  → puerto 8000
Service B1 → puerto 8001
Service B2 → puerto 8002
```

Se deben abrir tres terminales con el entorno virtual activado.

**Terminal 1 — Service B1:**

```bash
uvicorn service_b.main:app --port 8001
```

**Terminal 2 — Service B2:**

```bash
uvicorn service_b.main:app --port 8002
```

**Terminal 3 — Service A:**

```bash
uvicorn service_a.main:app --port 8000
```

Swagger de Service A:

`http://localhost:8000/docs`

Swagger de B1:

`http://localhost:8001/docs`

Swagger de B2:

`http://localhost:8002/docs`

---

## Demo

La demo permite observar:

* **Autenticación**
* **Límite de acceso**
* **Re-intentos**
* **Replicación**

### 1. Autenticación

Desde Swagger de Service A:

`http://localhost:8000/docs`

Se pueden probar los endpoints protegidos con:

```text
Usuario: admin
Contraseña: 1234
```

Las credenciales incorrectas son rechazadas.

### 2. Límite de acceso

El límite de acceso es de **3 solicitudes por minuto** para los endpoints protegidos. Al superar el límite, las solicitudes posteriores son rechazadas temporalmente.

### 3. Re-intentos y replicación

Las tácticas se prueban mediante:

`http://localhost:8000/saludo`

Service A intenta comunicarse primero con B1. Si B1 falla, realiza hasta **3 reintentos**. Si continúa fallando, utiliza B2 como instancia replicada.

Las fallas pueden provocarse de dos formas:

* Deteniendo B1 temporalmente.
* Configurando una probabilidad de disponibilidad.

Para utilizar la segunda opción, desde Swagger de B1:

`http://localhost:8001/docs`

ejecutar `POST /config` con:

```json
{
    "prob": 0.5
}
```

Esto establece una probabilidad de disponibilidad del **50 %**, permitiendo provocar fallas temporales sin detener el servicio.

Los eventos de reintentos y replicación se registran en:

```text
service_a/logs/service_a.log
```

---

## Pruebas con k6

El script se encuentra en:

```text
k6/script.js
```

Actualmente realiza **10 solicitudes**, utilizando **1 usuario virtual**, contra:

`http://localhost:8000/saludo`

Para ejecutarlo:

```bash
k6 run k6/script.js
```

Durante la ejecución se puede detener B1 o configurar su probabilidad de disponibilidad en `0.5` para observar los reintentos y la utilización de B2.

---

## Ejecución con Docker

Docker Compose crea los mismos tres servicios:

```text
service_a  → puerto 8000
service_b1 → puerto 8001
service_b2 → puerto 8002
```

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Swagger de Service A:

`http://localhost:8000/docs`

Las tácticas se prueban de la misma manera que en la ejecución local.

Para detener B1:

```bash
docker compose stop service_b1
```

Para volver a iniciarlo:

```bash
docker compose start service_b1
```

También se puede utilizar `POST /config` desde Swagger de B1 para establecer una probabilidad de disponibilidad de `0.5`.

Los logs de Service A se encuentran en:

```text
service_a/logs/service_a.log
```

### Pruebas con k6 en Docker

Con Docker Compose ejecutándose, desde otra terminal:

```bash
k6 run k6/script.js
```

Las solicitudes se realizan contra:

```text
http://localhost:8000/saludo
```

### Detener los servicios

```bash
docker compose down
```

---

## Fuentes

* Ander Fernández — [Cómo crear una API en Python](https://anderfernandez.com/blog/como-crear-api-en-python/)
* FastAPI — [Tutorial](https://fastapi.tiangolo.com/tutorial/)
* Docker — [Python Language-Specific Guide](https://docs.docker.com/guides/python/)
* Grafana k6 — [Documentación](https://grafana.com/docs/k6/)
