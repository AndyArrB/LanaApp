from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Transaccion, Presupuesto, Usuario
from database import get_session
from typing import List
from sqlalchemy.sql import func
from schemas import TransaccionUpdate, TransaccionCreate



router = APIRouter(prefix="/transacciones", tags=["Transacciones"])


#PARA CREAR UNA NUEVA TRANSACCIÓN
@router.post("/", response_model=Transaccion)
def crear_transaccion(transaccion: TransaccionCreate, session: Session = Depends(get_session)):
    nueva_transaccion = Transaccion(**transaccion.model_dump())
    session.add(nueva_transaccion)
    session.commit()
    session.refresh(nueva_transaccion)

    mes = nueva_transaccion.fecha.month
    anio = nueva_transaccion.fecha.year

    # busca si hay coincidencia con algún presupuesto
    presupuesto = session.exec(
        select(Presupuesto).where(
            Presupuesto.usuario_id == nueva_transaccion.usuario_id,
            Presupuesto.categoria_id == nueva_transaccion.categoria_id,
            Presupuesto.mes == mes,
            Presupuesto.anio == anio
        )
    ).first()

    if presupuesto:
        # Buscar transacciones de ese mes y categoría
        transacciones_mes = session.exec(
            select(Transaccion).where(
                Transaccion.usuario_id == nueva_transaccion.usuario_id,
                Transaccion.categoria_id == nueva_transaccion.categoria_id,
                func.strftime("%m", Transaccion.fecha) == f"{mes:02}",
                func.strftime("%Y", Transaccion.fecha) == str(anio)
            )
        ).all()

        suma = sum(t.monto for t in transacciones_mes)
        # valida si se está excediendo o no el presupuesto
        if suma > presupuesto.monto_maximo:
            aviso = f"¡Presupuesto excedido! Total gastado: {suma}, Límite: {presupuesto.monto_maximo}"

    return {
        "transaccion": nueva_transaccion,
        "aviso": aviso
    }


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
def actualizar_transaccion(transaccion_id: int, data: TransaccionUpdate, session: Session = Depends(get_session)):
    db_transaccion = session.get(Transaccion, transaccion_id)
    if not db_transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
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
    return {"msg": "Transacción eliminada correctamente"}