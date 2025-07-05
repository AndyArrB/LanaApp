# 💸 Lana App - Backend

**Lana App** es una aplicación móvil pensada para ayudarte a gestionar tus finanzas personales de forma fácil e intuitiva. Este repositorio contiene el backend desarrollado con **FastAPI** y **SQLModel**, encargado de manejar las operaciones principales como:

- Registro e inicio de sesión de usuarios
- Gestión de transacciones (ingresos y egresos)
- Creación y seguimiento de presupuestos mensuales
- Administración de pagos fijos
- Visualización de datos para gráficas
- Control de categorías personalizadas

Este proyecto forma parte de una entrega académica para la materia de Programación Móvil en la Universidad Politécnica de Querétaro.

---

## 🚀 Tecnologías utilizadas

- **FastAPI** como framework principal
- **SQLModel** para modelos de datos y ORM
- **SQLite** como base de datos local (puede cambiarse fácilmente a PostgreSQL u otra)
- **JWT (JSON Web Tokens)** para autenticación
- **Uvicorn** como servidor ASGI
- **Pydantic v2** para validación de datos

---

## ⚙️ Requisitos previos

- Python 3.11 o superior
- pip 

---

## 📦 Instalación y ejecución local

1. **Clona el repositorio**
   ```terminal
   git clone https://github.com/AndyArrB/LanaApp.git
   cd lana_backend
2. **Crea un entorno virtual**
   ```terminal
   python -m venv venv
   venv\Scripts\activate
3. **Instala las dependencias necesarias**
   ```terminal
   pip install -r requirements.txt
4. **Inicia el servidor**
   ```terminal
   uvicorn main:app --reload
5. **Accede a la URL**
   ```terminal
   http://localhost:8000/docs

---

## 📌 Notas adicionales
- El proyecto ya está listo para conectarse a un Front de React Native
- En caso de no poder ejecutar alguna parte del código, buscar a Andy.

---

## 📁 Estructura del proyecto
   ```bash
   lana_backend/
   │
   ├── main.py                  # Punto de entrada de la app FastAPI
   ├── database.py              # Conexión a la base de datos
   ├── models.py                # Tablas de la base de datos con SQLModel
   ├── schemas.py               # Validaciones con Pydantic
   ├── auth.py                  # Funciones de autenticación (JWT, hashing)
   ├── routes/                  # Endpoints organizados por funcionalidad
   │   ├── usuarios.py
   │   ├── transacciones.py
   │   ├── presupuestos.py
   │   ├── pagos_fijos.py
   │   ├── categorias.py
   │   └── graficas.py
   └── requirements.txt

