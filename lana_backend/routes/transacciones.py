from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Transaccion
from database import get_session
from typing import List

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])


#PARA CREAR UNA NUEVA TRANSACCIÓN
@router.post("/", response_model=Transaccion)
def crear_transaccion(transaccion: Transaccion, session: Session = Depends(get_session)):
    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)
    return transaccion


#PARA LISTAR LAS TRANSACCIONES
@router.get("/", response_model=List[Transaccion])
def listar_transacciones(session: Session = Depends(get_session)):
    return session.exec(select(Transaccion)).all()


#PARA OBTENER UNA TRANSACCIÓN POR EL ID
@router.get("/{transaccion_id}", response_model=Transaccion)
def obtener_transaccion(transaccion_id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


#PARA ACTUALIZAR UNA TRANSACCIÓN YA EXISTENTE
@router.put("/{transaccion_id}", response_model=Transaccion)
def actualizar_transaccion(transaccion_id: int, data: Transaccion, session: Session = Depends(get_session)):
    db_transaccion = session.get(Transaccion, transaccion_id)
    if not db_transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_transaccion, key, value)
    session.commit()
    return db_transaccion


#PARA ELIMINAR UNA TRANSACCION YA EXISTENTE
@router.delete("/{transaccion_id}")
def eliminar_transaccion(transaccion_id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    session.delete(transaccion)
    session.commit()
    return {"ok": True}