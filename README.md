# 🎓 Sistema de Gestión de Tutorías

Este proyecto es un sistema para la gestión de tutorías, desarrollado con **Vue.js** (utilizando **Tailwind CSS**) en el frontend y **FastAPI** en el backend. Sigue las instrucciones a continuación para configurarlo y ponerlo en marcha.

---

## 🔧 Requisitos previos

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas en tu sistema:

- **Node.js** (versión 16 o superior).
- **Python** (versión 3.8 o superior).
- **pip** (el gestor de paquetes de Python).
- **MySQL** o una base de datos compatible.

---

## 🚀 Instalación

Sigue los pasos para configurar ambos entornos, el del frontend y el del backend.

### 1️⃣ Configuración del Frontend (Vue.js con Tailwind CSS)

1.  Navega al directorio del frontend:
    ```bash
    cd frontend
    ```
2.  Instala las dependencias del proyecto:
    ```bash
    npm install
    ```
3.  Para iniciar el servidor de desarrollo, ejecuta:
    ```bash
    npm run dev
    ```
    Esto levantará el servidor del frontend, que estará disponible por defecto en **`http://localhost:5173`** (el puerto puede variar).

### 2️⃣ Configuración del Backend (FastAPI)

1.  Navega al directorio del backend:
    ```bash
    cd backend
    ```
2.  Crea y activa un entorno virtual para aislar las dependencias:
    ```bash
    # Crear el entorno virtual
    python -m venv .venv
    ```
    Ahora, activa el entorno. El comando varía según tu sistema operativo:
    - **En Windows (PowerShell/CMD):**
      ```bash
      .\venv\Scripts\activate
      ```
    - **En macOS / Linux:**
      ```bash
      source venv/bin/activate
      ```
3.  Con el entorno virtual activado, instala todas las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configura las variables de entorno. Copia el archivo `.env.example` y renómbralo a `.env`:
    ```bash
    cp .env.example .env
    ```
    Abre el nuevo archivo `.env` y actualiza las credenciales de tu base de datos:
    ```env
    # Variables de entorno para la Base de Datos
    DB_USER="tu_usuario_mysql"
    DB_PASSWORD="tu_contraseña_segura"
    DB_HOST="localhost"
    DB_PORT="3306"
    DB_NAME="nombre_de_tu_base_de_datos"
    ```
5.  Levanta el servidor de desarrollo de FastAPI:
    ```bash
    # Asumiendo que tu archivo principal es app/main.py
    fastapi dev app/main.py
    ```
    El backend estará disponible en **`http://127.0.0.1:8000`**. Puedes acceder a la documentación interactiva en **`http://127.0.0.1:8000/docs`**.

---

## 💡 Notas importantes

- **Ejecución simultánea**: Asegúrate de que los servidores de **Vue.js** y **FastAPI** estén corriendo al mismo tiempo para que el sistema funcione correctamente.

---

## 🛠️ Tecnologías utilizadas

#### **Frontend**

- **Framework**: Vue.js 3
- **Estilos**: Tailwind CSS
- **Herramienta de construcción**: Vite

#### **Backend**

- **Framework**: FastAPI
- **ORM / Modelado de datos**: SQLModel, Pydantic

#### **Base de datos**

- **Motor principal**: MySQL

---

## 📞 Contacto

Si tienes preguntas o problemas, no dudes en contactarnos. ¡Estamos aquí para ayudarte! ✨
