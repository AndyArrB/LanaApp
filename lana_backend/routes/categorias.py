from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from schemas import CategoriaCreate, CategoriaRead
from models import Categoria
from typing import List

router = APIRouter(prefix="/categorias", tags=["Categorías"])


#RUTA PARA CREAR CATEGORIA NUEVA
@router.post("/", response_model=CategoriaRead)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_session)):
    existente = db.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()
    if existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    nueva_categoria = Categoria(nombre=categoria.nombre)
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
