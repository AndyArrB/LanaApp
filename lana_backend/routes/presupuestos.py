from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from models import Presupuesto
from database import get_session
from schemas import PresupuestoCreate, PresupuestoUpdate

router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])


# PARA CREAR UN NUEVO PRESUPUESTO
@router.post("/", response_model=Presupuesto)
def crear_presupuesto(presupuesto: PresupuestoCreate, session: Session = Depends(get_session)):
    session.add(presupuesto)
    session.commit()
    session.refresh(presupuesto)
    return presupuesto


# PARA LISTAR TODOS LOS PRESUPUESTOS ACTUALES
@router.get("/", response_model=List[Presupuesto])
def listar_presupuestos(session: Session = Depends(get_session)):
    return session.exec(select(Presupuesto)).all()


#PARA BUSCAR UNO ESPECIFICO
@router.get("/{presupuesto_id}", response_model=Presupuesto)
def obtener_presupuesto(presupuesto_id: int, session: Session = Depends(get_session)):
    presupuesto = session.get(Presupuesto, presupuesto_id)
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    return presupuesto


# PARA ACTUALIZAR UN PRESUPUESTO EXISTENTE
@router.put("/{presupuesto_id}", response_model=Presupuesto)
def actualizar_presupuesto(presupuesto_id: int, data: PresupuestoUpdate, session: Session = Depends(get_session)):
    presupuesto = session.get(Presupuesto, presupuesto_id)
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(presupuesto, key, value)
    session.commit()
    return presupuesto


# PARA ELIMINAR UN PRESUPUESTO EXSIETNTE
@router.delete("/{presupuesto_id}")
def eliminar_presupuesto(presupuesto_id: int, session: Session = Depends(get_session)):
    presupuesto = session.get(Presupuesto, presupuesto_id)
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    session.delete(presupuesto)
    session.commit()
    return {"ok": True}
