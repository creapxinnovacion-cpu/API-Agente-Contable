# API Agente Contable 🚀

Este es el backend para la plataforma SaaS de contabilidad y procesamiento de Documentos Tributarios Electrónicos (DTE). Está construido bajo un enfoque moderno y modular utilizando **FastAPI**, **SQLAlchemy (ORM)** y validación estructurada basada en **Pydantic**. 

---

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado en las siguientes capas y carpetas para mantener un flujo de trabajo limpio y escalable (separación de responsabilidades):

* **`db/`**: Configuración e instanciación de conexión a la base de datos y definiciones maestras de los *engines*. (Actualmente configurado con SQLite, listo para migrar a PostgreSQL/Neon).
* **`models/`**: Todo el esquema de persistencia mediante SQLAlchemy. Representaciones uno a uno de las estructuras reales de las tablas en SQL.
* **`schemas/`**: Modelos Pydantic. Sirven como contratos de datos precisos para gobernar las entradas (*Requests*) y salidas (*Responses*) de cada endpoint.
* **`services/`**: Contiene exclusivamente la lógica de negocio pura y la funcionalidad CRUD, abstraída del enrutamiento web asíncrono.
* **`routers/`**: Exposición directa de los endpoints. Gestionan las peticiones HTTP, validan a través de los esquemas y llaman a la respectiva lógica de servicios.
* **`main.py`**: El corazón y punto de entrada de la aplicación FastAPI. Instancia la aplicación principal, agrupa y registra los diferentes *routers* y despliega la documentación de Swagger de manera automática.

---

## 🛠️ Instalación y Configuración

Asegúrate de contar con **Python 3.10+** instalado en tu sistema local.

1. **Clona o ubícate en el directorio matriz:**
   ```bash
   cd API-Agente-Contable
   ```

2. **Crea y activa el entorno virtual virtual:**
   * En Windows (PowerShell): 
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * En Linux/Mac: 
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Instala los requerimientos definidos:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configura tus variables de entorno:**
   * Renombra o copia el archivo `.env.example` a `.env` en la raíz del proyecto.
   * Abre `.env` y sustituye la variable `DATABASE_URL` por la cadena de conexión real de NeonDB:
   ```env
   DATABASE_URL="postgresql://usuario:password@host-de-neon.aws.neon.tech/neondb?sslmode=require"
   SECRET_KEY="TU_CLAVE_SECRETA_PERSONALIZADA"
   ```

---

## 🚀 Despliegue Local

Para lanzar tu servidor de integración en un entorno de desarrollo con *hot-reloading* habilitado:

```bash
uvicorn main:app --reload
```

Una vez que Uvicorn haya iniciado el servidor, podrás acceder a:

* **Endpoint Raíz (Estado Vital):** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Health Check API/BD:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
* 📖 **Documentación Swagger UI (Explorador Interactivo):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* 📖 **Documentación ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Estructura Actual de la Base de Datos

Cuenta con los siguientes modelos fundamentales definidos, ya conectados y relacionados:

* `Empresa` -> Información constitutiva para los *Tenants* u organizaciones contables.
* `Usuario` -> Gestión y almacenamiento de las credenciales de los distintos operadores.
* `UsuarioEmpresa` -> Tabla intermedia encargada de gestionar los roles asignados de cada Usuario hacia múltiples y diferentes Empresas.

---

## 🛡️ Autenticación y Seguridad (JWT)

El sistema ya implementa un flujo de seguridad en producción:
- **Hash de Contraseñas:** Integración de la biblioteca `passlib[bcrypt]` en el servicio `auth_service.py` para encriptar los passwords antes de guardarlos a la BD.
- **Emisión de Tokens:** Endpoint `/auth/login` activo. Valida credenciales con la BD e instancia un *JSON Web Token* utilizando `python-jose`. 
- **Payload JWT Personalizado:** El token fue modelado no solo para portar la autorización, sino para inyectar vitalidad en el Frontend. Lleva intrínseco el rol (`is_admin`), el ID de la tabla `Empresa`, y crucialmente el `nitEmpresa`, que es consumido por las interfaces de React para su lógica de autodetección.

---

## 🔗 Integración cruzada (CORS)

Dado que la arquitectura se divide en la API en el puerto `8000` y el cliente React Vite en el puerto `5173`, el archivo matriz `main.py` incorpora internamente las políticas requeridas usando `CORSMiddleware`, habilitando peticiones directas provenientes del localhost.

---

## 🌱 Datos Iniciales (Seed)

Si necesitas arrancar el entorno rápidamente sin crear flujos de registro manuales en Postman o en el código, utiliza nuestro script:
```bash
python seed.py
```
Esta herramienta poblará la base de datos automáticamente con:
- Empresa *Mock*: **06140101801234**
- Usuario Test: **admin@creapx.com** // Pass: **admin123**
