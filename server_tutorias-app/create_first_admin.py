"""
Script de inicialización para crear el primer usuario administrador.

Proporciona una interfaz de línea de comandos para crear el administrador
inicial del sistema, con validación de usuarios duplicados y hashing seguro
de contraseñas.

Uso:
    python create_first_admin.py
"""

import getpass
from sqlmodel import Session, select

from app.database import engine
from app.models.administrador import Administrador
from app.core.security import get_password_hash


def create_admin_user():
    """
    Crea el primer usuario administrador del sistema de forma interactiva.
    
    Solicita nombre de usuario y contraseña de forma segura,
    valida que no exista un administrador con el mismo nombre,
    y crea el registro en la base de datos con contraseña hasheada.
    """
    print("--- Creación del primer usuario administrador ---")
    
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
        new_admin = Administrador(usuario=usuario, contraseña=hashed_password)
        
        session.add(new_admin)
        session.commit()
        
        print(f"¡Éxito! El administrador '{usuario}' ha sido creado.")


if __name__ == "__main__":
    create_admin_user()
