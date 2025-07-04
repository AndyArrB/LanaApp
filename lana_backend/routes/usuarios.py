from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Usuario
from database import get_session
from auth import encriptar_contrasena, verificar_contrasena, crear_token, verificar_token
from pydantic import BaseModel, EmailStr, constr
from typing import Annotated

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

NombreStr = Annotated[str, constr(min_length=3, strip_whitespace=True)]

class UsuarioRegistro(BaseModel):
    nombre: NombreStr
    apellido: NombreStr
    email: EmailStr
    password: Annotated[str, constr(min_length=8)]
    
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
    

# PARA REGISTRAR UN NUEVO USUARIO
@router.post("/registro")
def registrar_usuario(data: UsuarioRegistro, session: Session = Depends(get_session)):
    existe = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    nuevo = Usuario(
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        hashed_password=encriptar_contrasena(data.password)
        )
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return {"msg": "Usuario registrado correctamente", "id": nuevo.id}


#PARA INICIAR SESIÓN (OSEA CUANDO YA TENGO CUENTA)
@router.post("/login")
def login(data: UsuarioLogin, session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
    if not usuario or not verificar_contrasena(data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}


#PARA VER QUE USUARIOS HAY EN LA BD
@router.get("/usuarios/", response_model=list[Usuario])
def listar_usuarios(session: Session = Depends(get_session)):
    usuarios = session.exec(select(Usuario)).all()
    return usuarios


# PARA BUSCAR UN USUARIO EN EESPECÍFICO
@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


#PARA ELIMINAR UN USUARIO EXISTENTE
@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}
