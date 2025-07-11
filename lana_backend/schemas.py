from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

#VALIDACIONES PARA TRANSACCION BASICAS
class TransaccionBase(BaseModel):
    monto: Optional[float] = Field(None, gt=0, description="El monto debe ser mayor a cero")
    categoria_id: Optional[int]
    fecha: Optional[date]
    descripcion: Optional[str] = None
    tipo: Optional[str]
    usuario_id: Optional[int]
    
    
    @field_validator("fecha")
    def validar_fecha(cls, v):
        if v is not None and v > date.today():
            raise ValueError("La fecha no puede ser futura")
        return v
    
    @field_validator("tipo")
    def validar_tipo(cls, v):
        if v is not None and v.lower() not in ("ingreso", "egreso"):
            raise ValueError("El tipo debe ser 'ingreso' o 'egreso'")
        return v.lower() if v else v


#MODELO EN TRANSACCIONES NUEVAS
class TransaccionCreate(TransaccionBase):
    monto: float
    categoria_id: int
    fecha: date
    tipo:str
    usuario_id: int

#PASO LO MISMO PERO PARA ACTUALIZAR TRANSACCIONES
class TransaccionUpdate(TransaccionBase):
    pass



#VALIDACIONES PARA LOS PRESUPUESTOS
class PresupuestoBase(BaseModel):
    usuario_id: Optional[int]
    categoria_id: Optional[int]
    monto_maximo: Optional[float] = Field(None, gt=0, description="El monto debe ser mayo a cero")
    mes: Optional[int] = Field(None, ge=1, le=12, description="Meses de Enero (1) a Diciembre (12)")
    anio: Optional[int] = Field(None, ge=2025, le=2025, description="Solo para el año en curso")
    
    
    @field_validator("anio")
    def validar_anio(cls, v):
        if v is not None and v > date.today().year + 1:
            raise ValueError("El año no puede ser mayor al año actual")
        return v
    

#MODELO CON NUEVOS PRESUPUESTOS
class PresupuestoCreate(PresupuestoBase):
    usuario_id: int
    categoria_id: int
    monto_maximo: float
    mes: Optional[int] = None
    anio: Optional[int] = None
    
#PARA ACTUALIZAR PRESUPUESTOS
class PresupuestoUpdate(PresupuestoBase):
    pass


#VALIDACIONES PARA PAGOS FIJOS
class PagoFijoBase(BaseModel):
    descripcion: str
    monto: float
    categoria_id: int
    frecuencia: str  # osea si será mensual o quincenal
    proxima_fecha: date
    usuario_id: int

    @field_validator("monto")
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return v
    
    @field_validator("frecuencia")
    def frecuencia_valida(cls, v):
        if v.lower() not in ("mensual", "quincenal"):
            raise ValueError("La frecuencia debe ser 'mensual' o 'quincenal'")
        return v.lower()
    
    @field_validator("descripcion")
    def descripcion_no_vacia(cls, v):
        if not v.strip():
            raise ValueError("La descripción no puede estar vacía")
        return v.strip()

class PagoFijoCreate(PagoFijoBase):
    pass 

class PagoFijoUpdate(PagoFijoBase):
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    frecuencia: Optional[str] = None
    proxima_fecha: Optional[date] = None
    
    
# PARA CATEGORIAS
class CategoriaBase(BaseModel):
    nombre: str
    usuario_id: int

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaRead(CategoriaBase):
    id: int

class CategoriaUpdate(CategoriaBase):
    nombre: Optional[str] = None
    usuario_id: Optional[int] = None
    
    @field_validator("nombre")
    def validar_nombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v