"""
Script de inicialización para crear el primer usuario administrador.

Proporciona una interfaz de línea de comandos para crear el administrador
inicial del sistema (SUPER_ADMIN), con validación de usuarios duplicados 
y hashing seguro de contraseñas.

Uso:
    python -m utils.create_first_admin
"""
import sys
import os
import getpass
from sqlmodel import Session, select

# Agregamos el directorio padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine
from app.models.administrador import Administrador, RolAdministrador # Importamos el Enum
from app.core.security import get_password_hash

def create_admin_user():
    """
    Crea el primer usuario administrador (SUPER_ADMIN) del sistema de forma interactiva.
    """
    print("--- Creación del primer usuario administrador (SUPER_ADMIN) ---")
    
    usuario = input("Introduce el nombre de usuario para el administrador: ")
    contraseña = getpass.getpass("Introduce la contraseña para el administrador: ")
    
    with Session(engine) as session:
        existing_admin = session.exec(
            select(Administrador).where(Administrador.usuario == usuario)
        ).first()
        
        if existing_admin:
            print(f"Error: El usuario '{usuario}' ya existe.")
            return
        
        hashed_password = get_password_hash(contraseña)
        
        # AQUÍ ESTÁ EL CAMBIO CLAVE:
        # Asignamos explícitamente el rol SUPER_ADMIN para garantizar permisos totales.
        new_admin = Administrador(
            usuario=usuario, 
            contraseña=hashed_password,
            rol=RolAdministrador.SUPER_ADMIN, # <--- Garantizamos el rol
        )
        
        session.add(new_admin)
        session.commit()
        
        print(f"\n¡Éxito! El administrador '{usuario}' ha sido creado con rol SUPER_ADMIN.")

if __name__ == "__main__":
    create_admin_user()