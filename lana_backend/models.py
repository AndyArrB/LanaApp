from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

#TABLA DE TRANSACCIONES
class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto: float
    categoria_id: int
    fecha: date
    descripcion: Optional[str]
    tipo: str #Esto es para saber si será un ingreso o un egreso
    usuario_id: int
    
    
#TABLA DE USUARIOS
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str = Field(unique=True, index=True)
    hashed_password: str


# TABLS DE PRESUPUESTOS
class Presupuesto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int
    categoria_id: int
    monto_maximo: float
    mes: int
    anio: int
    

#TABLA DE PAGOS FIJOS
class PagoFijo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    monto: float
    categoria_id: int
    frecuencia: str
    proxima_fecha: date
    usuario_id: int
    

#TABLA DE CATEGORIAS
class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
