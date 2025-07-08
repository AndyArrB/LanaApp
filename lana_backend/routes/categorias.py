from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from schemas import CategoriaCreate, CategoriaRead
from models import Categoria
from typing import List
from sqlalchemy import func

router = APIRouter(prefix="/categorias", tags=["Categorías"])


# RUTA PARA CREAR CATEGORIA NUEVA
@router.post("/", response_model=CategoriaRead)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_session)):
    # Validar que no exista una categoría con ese nombre para el mismo usuario (sin distinguir mayúsculas/minúsculas)
    existente = db.exec(
        select(Categoria)
        .where(
            func.lower(Categoria.nombre) == categoria.nombre.lower(),
            Categoria.usuario_id == categoria.usuario_id
        )
    ).first()
    
    if existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe para este usuario")

    # Crear y guardar
    nueva_categoria = Categoria(
        nombre=categoria.nombre.strip(),
        usuario_id=categoria.usuario_id
    )
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

#RUTA PARA LISTAR LAS CATEGORIAS EXISTENTES
@router.get("/", response_model=List[CategoriaRead])
def listar_categorias(db: Session = Depends(get_session)):
    categorias = db.exec(select(Categoria)).all()
    return categorias


#RUTA PARA LISTAR SOLO UNA CATEGORIA ESPECÍFICA
@router.get("/{categoria_id}", response_model=CategoriaRead)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_session)):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


# RUTA PARA ELIMINAR UNA CATEGORIA
@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_session)):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada correctamente"}
