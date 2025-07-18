from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.sql import func
from database import get_session
from models import Transaccion, Presupuesto, Categoria

router = APIRouter(prefix="/graficas", tags=["Gráficas"])


#GRAFICA DE GASTOS POR CADA CATEGORIA
@router.get("/gastosCategoria")
def gastos_por_categoria(usuario_id: int, session: Session = Depends(get_session)):
    resultados = session.exec(
        select(Transaccion.categoria_id, Categoria.nombre, func.sum(Transaccion.monto))
        .join(Categoria, Transaccion.categoria_id == Categoria.id)
        .where(Transaccion.usuario_id == usuario_id)
        .group_by(Transaccion.categoria_id)
    ).all()

    return [{"categoria_id": r[0], "nombre": r[1], "total": r[2]} for r in resultados]


#GRAFICA DE INGRESOS Y EGRESOS
@router.get("/ingresosEgresos")
def ingresos_vs_egresos(usuario_id: int, session: Session = Depends(get_session)):
    query = select(
        func.strftime("%Y-%m", Transaccion.fecha).label("mes"),
        Transaccion.tipo,
        func.sum(Transaccion.monto).label("total")
    ).where(
        Transaccion.usuario_id == usuario_id
    ).group_by("mes", Transaccion.tipo).order_by("mes")

    resultados = session.exec(query).all()

    data = {}
    for mes, tipo, total in resultados:
        if mes not in data:
            data[mes] = {"ingresos": 0, "egresos": 0}
        data[mes][f"{tipo}s"] = total

    return [{"mes": k, **v} for k, v in data.items()]


#GRAFICA DEL PRESUPUESTO Y LO QUE SE HA GASTADO AL MOMENTO
@router.get("/presupuestoGastos")
def presupuesto_vs_gasto(usuario_id: int, mes: int, anio: int, session: Session = Depends(get_session)):
    presupuestos = session.exec(
        select(Presupuesto).where(
            Presupuesto.usuario_id == usuario_id,
            Presupuesto.mes == mes,
            Presupuesto.anio == anio
        )
    ).all()

    resultados = []
    for p in presupuestos:
        suma_gastos = session.exec(
            select(func.sum(Transaccion.monto)).where(
                Transaccion.usuario_id == usuario_id,
                Transaccion.categoria_id == p.categoria_id,
                Transaccion.tipo == "egreso",
                func.strftime("%m", Transaccion.fecha) == f"{mes:02}",
                func.strftime("%Y", Transaccion.fecha) == str(anio)
            )
        ).first() or 0

        resultados.append({
            "categoria": p.categoria_id,
            "presupuesto": p.monto_maximo,
            "gastado": suma_gastos
        })

    return resultados