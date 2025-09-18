# routers/tutores.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from typing import List

# ⚙️ Imports refactorizados
from app.database import get_session
from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate, TutorRead, TutorLogin # 👈 Se importa TutorLogin
from app.services import tutor_service # 👈 Importamos nuestro nuevo servicio

router = APIRouter(prefix="/tutores", tags=["Tutores"])


# ✅ 1. Dependencia reutilizable para obtener el tutor o lanzar 404
def get_tutor_or_404(id_tutor: int, session: Session = Depends(get_session)) -> Tutor:
    tutor = session.get(Tutor, id_tutor)
    if not tutor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tutor no encontrado")
    return tutor


# 🔹 Obtener todos los tutores
@router.get("/", response_model=List[TutorRead])
def get_tutores(session: Session = Depends(get_session)):
    return session.exec(select(Tutor)).all()


# 🔹 Obtener tutor por ID
@router.get("/{id_tutor}", response_model=TutorRead)
def get_tutor(tutor: Tutor = Depends(get_tutor_or_404)):
    return tutor


# 🔹 Crear tutor
@router.post("/", response_model=TutorRead, status_code=status.HTTP_201_CREATED)
def create_tutor(data: TutorCreate, session: Session = Depends(get_session)):
    return tutor_service.create_tutor(db=session, data=data)


# 🔹 Actualizar tutor
@router.put("/{id_tutor}", response_model=TutorRead)
def update_tutor(
    data: TutorUpdate,
    tutor: Tutor = Depends(get_tutor_or_404),
    session: Session = Depends(get_session)
):
    return tutor_service.update_tutor(db=session, tutor=tutor, data=data)


# 🔹 Eliminar tutor
@router.delete("/{id_tutor}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tutor(tutor: Tutor = Depends(get_tutor_or_404), session: Session = Depends(get_session)):
    # ✅ 2. Respuesta estándar para eliminación
    session.delete(tutor)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 🔹 Login de tutor
@router.post("/login", response_model=TutorRead)
def login(data: TutorLogin, session: Session = Depends(get_session)):
    tutor = tutor_service.get_tutor_by_email(session, data.correo)

    if not tutor or not tutor_service.verify_password(data.contraseña, tutor.contraseña):
        # ✅ 3. Excepción estándar de "No autorizado"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ✅ 4. 🔒 Usamos TutorRead como response_model para NUNCA devolver el hash
    return tutor