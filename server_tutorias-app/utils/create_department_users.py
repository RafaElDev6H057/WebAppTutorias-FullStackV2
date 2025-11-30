import sys
import os

# Agregamos el directorio padre al path para poder importar los módulos de la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database import engine
from app.models.administrador import Administrador, RolAdministrador
from app.core.security import get_password_hash

def create_users():
    print("--- INICIANDO CREACIÓN DE USUARIOS DE DEPARTAMENTOS ---")
    
    # Definimos los usuarios que queremos crear
    # Puedes cambiar las contraseñas aquí si lo deseas
    users_to_create = [
        {
            "usuario": "psicologia",
            "password": "password123",
            "rol": RolAdministrador.PSICOLOGIA,
            "nombre": "Departamento",
            "apellido_p": "Psicología"
        },
        {
            "usuario": "ciencias_basicas",
            "password": "password123",
            "rol": RolAdministrador.CIENCIAS_BASICAS,
            "nombre": "Departamento",
            "apellido_p": "Ciencias Básicas"
        },
        {
            "usuario": "jefatura",
            "password": "password123",
            "rol": RolAdministrador.JEFATURA_ACADEMICA,
            "nombre": "Jefatura",
            "apellido_p": "Académica"
        }
    ]

    with Session(engine) as session:
        for user_data in users_to_create:
            # 1. Verificar si ya existe
            statement = select(Administrador).where(Administrador.usuario == user_data["usuario"])
            existing_user = session.exec(statement).first()

            if existing_user:
                print(f"[OMITIDO] El usuario '{user_data['usuario']}' ya existe.")
                
                # Opcional: Si quisieras actualizar el rol de un usuario existente para corregirlo:
                # if existing_user.rol != user_data["rol"]:
                #     print(f"   -> Actualizando rol de '{user_data['usuario']}' a {user_data['rol']}")
                #     existing_user.rol = user_data["rol"]
                #     session.add(existing_user)
                #     session.commit()
            
            else:
                # 2. Crear nuevo usuario
                print(f"[CREANDO] Creando usuario '{user_data['usuario']}' con rol '{user_data['rol'].value}'...")
                
                new_admin = Administrador(
                    usuario=user_data["usuario"],
                    contraseña=get_password_hash(user_data["password"]), # Importante: Hashing
                    rol=user_data["rol"]
                )
                
                session.add(new_admin)
                session.commit()
                print(f"   -> ¡Usuario '{user_data['usuario']}' creado exitosamente!")

    print("\n--- PROCESO FINALIZADO ---")
    print("Ahora puedes iniciar sesión con estos usuarios para probar los permisos.")

if __name__ == "__main__":
    create_users()