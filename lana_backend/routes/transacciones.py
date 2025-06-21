from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Transaccion, Usuario, Presupuesto
from database import get_session
from typing import List
from sqlalchemy.sql import func


router = APIRouter(prefix="/transacciones", tags=["Transacciones"])


#PARA CREAR UNA NUEVA TRANSACCIÓN
@router.post("/", response_model=Transaccion)
def crear_transaccion(transaccion: Transaccion, session: Session = Depends(get_session)):
    
    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)


    mes = transaccion.fecha.month
    anio = transaccion.fecha.year

    # busca si hay coincidencia con algun presupuesto
    presupuesto = session.exec(
        select(Presupuesto).where(
            Presupuesto.usuario_id == transaccion.usuario_id,
            Presupuesto.categoria == transaccion.categoria,
            Presupuesto.mes == mes,
            Presupuesto.anio == anio
        )
    ).first()

    if presupuesto:
        # Buscar transacciones de ese mes y categoría
        transacciones_mes = session.exec(
            select(Transaccion).where(
                Transaccion.usuario_id == transaccion.usuario_id,
                Transaccion.categoria == transaccion.categoria,
                func.strftime("%m", Transaccion.fecha) == f"{mes:02}",
                func.strftime("%Y", Transaccion.fecha) == str(anio)
            )
        ).all()

        suma = sum(t.monto for t in transacciones_mes)
        # valida si se está excediendo o no el presupuesto
        if suma > presupuesto.monto_maximo:
            print("Presupuesto excedido!")
            print(f"Total gastado: {suma}, Límite: {presupuesto.monto_maximo}")
            
    
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