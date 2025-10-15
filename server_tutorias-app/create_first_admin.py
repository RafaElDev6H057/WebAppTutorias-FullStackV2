# create_first_admin.py
import getpass
from sqlmodel import Session
from app.database import engine
from app.models.administrador import Administrador
from app.core.security import get_password_hash

def create_admin_user():
    print("--- Creación del primer usuario administrador ---")
    
    # Pedimos el nombre de usuario de forma interactiva
    usuario = input("Introduce el nombre de usuario para el administrador: ")
    
    # Pedimos la contraseña de forma segura (no se verá al escribir)
    contraseña = getpass.getpass("Introduce la contraseña para el administrador: ")
    
    # Creamos una sesión de base de datos
    with Session(engine) as session:
        # Verificamos si el usuario ya existe
        existing_admin = session.query(Administrador).filter(Administrador.usuario == usuario).first() #type: ignore
        if existing_admin:
            print(f"❌ Error: El usuario '{usuario}' ya existe.")
            return

        # Hasheamos la contraseña
        hashed_password = get_password_hash(contraseña)
        
        # Creamos el nuevo administrador
        new_admin = Administrador(usuario=usuario, contraseña=hashed_password)
        
        session.add(new_admin)
        session.commit()
        
        print(f"✅ ¡Éxito! El administrador '{usuario}' ha sido creado.")

if __name__ == "__main__":
    create_admin_user()