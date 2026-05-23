**Gestión de Gastos (FastAPI)**

Breve proyecto para gestionar gastos y usuarios usando FastAPI. Código parcial en desarrollo; incluye rutas de autenticación, posts, roles, usuarios y utilidades para AWS y migraciones con Alembic.

**Estado Actual**:
- **Código**: Implementación principal en [gestion_financiera_app/src](gestion_financiera_app/src)
- **Migraciones**: configuradas con Alembic en [gestion_financiera_app/alembic](gestion_financiera_app/alembic)
- **Dependencias**: definidas en [pyproject.toml](pyproject.toml) y [requirements](requirements)

**Estructura clave**
- **`gestion_financiera_app/src`**: código fuente (routers, servicios, modelos).
- **`gestion_financiera_app/alembic`**: scripts y configuración de migraciones.
- **`tests/`**: pruebas unitarias parciales para auth, aws y posts.

**Instalación (recomendado: Poetry)**

1. Instalar dependencias:

```bash
poetry install
```

2. (Opcional) activar el entorno:

```bash
poetry shell
```

**Ejecutar la aplicación**

Usando Uvicorn (desde la raíz del proyecto):

```bash
poetry run uvicorn gestion_financiera_app.src.main:app --reload --host 127.0.0.1 --port 8000
```

La API quedará disponible en `http://127.0.0.1:8000` y la documentación automática en `/docs`.

**Migraciones (Alembic)**

Usar el archivo de configuración de Alembic incluido. Por ejemplo, para aplicar migraciones:

```bash
alembic -c gestion_financiera_app/alembic.ini upgrade head
```

Para generar una nueva migración (autogenerada):

```bash
alembic -c gestion_financiera_app/alembic.ini revision --autogenerate -m "mensaje"
```

**Pruebas**

Ejecutar las pruebas con:

```bash
poetry run pytest -q
```

**Variables de entorno / Configuración**

- Recomendable crear un fichero `.env` para credenciales (DB, AWS, SECRET_KEY). No hay fichero `.env` en el repositorio por seguridad.
- Configuración principal en [gestion_financiera_app/src/core/config.py](gestion_financiera_app/src/core/config.py)

**Dónde mirar primero**
- Punto de entrada: [gestion_financiera_app/src/main.py](gestion_financiera_app/src/main.py)
- Rutas y lógica: carpetas `auth/`, `users/`, `posts/`, `roles/` bajo `gestion_financiera_app/src`

**Contribuir**
- Abrir issues o PRs con cambios pequeños y pruebas cuando sea posible.

---

