# app/database.py

from sqlmodel import SQLModel, create_engine, Session

# 1. Definimos la URL para la base de datos SQLite.
# Esto creará un archivo llamado "database.db" en la raíz de tu proyecto.
DATABASE_URL = "sqlite:///./database.db"

# 2. Creamos el "engine" con un argumento especial para SQLite.
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

# Esta función no necesita cambios.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Esta función tampoco necesita cambios.
def get_session():
    with Session(engine) as session:
        yield session