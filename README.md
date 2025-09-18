# 🎓 Sistema de Gestión de Tutorías

Este proyecto es un sistema para la **gestión de tutorías**, desarrollado con **Vue.js** (utilizando **Tailwind CSS** para el diseño) en el frontend y **Laravel** en el backend. Sigue las instrucciones a continuación para configurarlo y ponerlo en marcha.

---

## 🔧 **Requisitos previos**

Antes de comenzar, asegúrate de tener instaladas las siguientes herramientas en tu sistema:

- [Node.js](https://nodejs.org/) (versión 16 o superior).
- [Composer](https://getcomposer.org/) (versión 2 o superior).
- [PHP](https://www.php.net/) (versión 8.1 o superior).
- [MySQL](https://www.mysql.com/) o cualquier base de datos compatible con Laravel.

---

## 🚀 **Instalación**

### 1️⃣ **Configuración del Frontend (Vue.js con Tailwind CSS)**

1. Navega al directorio del frontend:

   ```bash
   cd frontend
   ```

2. Instala las dependencias:

   ```bash
   npm install
   ```

3. Para iniciar el servidor de desarrollo, ejecuta:
   ```bash
   npm run dev
   ```
   Esto levantará el servidor del frontend, que estará disponible por defecto en http://localhost:5173 (el puerto puede variar).

### 2️⃣ **Configuración del Backend (Laravel)**

1. Navega al directorio del backend:

   ```bash
   cd backend
   ```

2. Instala las dependencias de Laravel:

   ```bash
   composer install
   ```

3. Configura el entorno:

   - Copia el archivo `.env.example` y renómbralo a `.env`:
     ```bash
     cp .env.example .env
     ```
   - Abre el archivo `.env` en un editor de texto y actualiza las credenciales de tu base de datos:
     ```env
     DB_CONNECTION=mysql
     DB_HOST=127.0.0.1
     DB_PORT=3306
     DB_DATABASE=nombre_de_tu_base
     DB_USERNAME=tu_usuario
     DB_PASSWORD=tu_contraseña
     ```

4. Genera la clave de la aplicación:

   ```bash
   php artisan key:generate
   ```

5. Ejecuta las migraciones para crear las tablas necesarias en la base de datos:

   ```bash
   php artisan migrate
   ```

6. Levanta el servidor de desarrollo:
   ```bash
   php artisan serve
   ```
   El backend estará disponible por defecto en http://localhost:8000.

## 💡 **Notas importantes**

- **Ejecución simultánea**: Asegúrate de que los servidores de **Vue.js** y **Laravel** estén corriendo al mismo tiempo para que el sistema funcione correctamente.
- **Permisos de Laravel**: Si encuentras problemas de permisos, ejecuta:
  ```bash
  sudo chmod -R 775 storage bootstrap/cache
  ```

## 🛠️ **Tecnologías utilizadas**

### Frontend

- **Framework**: Vue.js 3
- **Estilos**: Tailwind CSS
- **Herramienta de construcción**: Vite

### Backend

- **Framework**: Laravel
- **ORM**: Eloquent

### Base de datos

- **Motor principal**: MySQL

## 📞 **Contacto**

Si tienes preguntas o problemas, no dudes en contactarnos. ¡Estamos aquí para ayudarte! ✨
