from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import PagoFijo
from schemas import PagoFijoCreate, PagoFijoUpdate
from typing import List

router = APIRouter(prefix="/pagos-fijos", tags=["Pagos Fijos"])


#RUTA PARA CREAR UN NUEVO PAGO FIJO
@router.post("/", response_model=PagoFijo)
def crear_pago_fijo(data: PagoFijoCreate, session: Session = Depends(get_session)):
    nuevo = PagoFijo(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


#RUTA OARA LOSTAR TODOS LOS PAGOS FIJOS
@router.get("/", response_model=List[PagoFijo])
def listar_pagos_fijos(session: Session = Depends(get_session)):
    return session.exec(select(PagoFijo)).all()


#RUTA PARA BUSCAR UN PAGO FIJO EN ESPECIFICO
@router.get("/{pago_id}", response_model=PagoFijo)
def obtener_pago_fijo(pago_id: int, session: Session = Depends(get_session)):
    pago = session.get(PagoFijo, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago fijo no encontrado")
    return pago


#RUTA PARA ACTUALIZAR UN PAGO YA EXISTENTE
@router.put("/{pago_id}", response_model=PagoFijo)
def actualizar_pago_fijo(pago_id: int, data: PagoFijoUpdate, session: Session = Depends(get_session)):
    pago = session.get(PagoFijo, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago fijo no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(pago, key, value)
    session.commit()
    return pago


#RUTA PARA ELIMINAR UN PAGO EXISTENTE
@router.delete("/{pago_id}")
def eliminar_pago_fijo(pago_id: int, session: Session = Depends(get_session)):
    pago = session.get(PagoFijo, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago fijo no encontrado")
    session.delete(pago)
    session.commit()
    return {"ok": True}