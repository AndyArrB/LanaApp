from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuración principal
SECRET_KEY = "holacomoestas"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PARA ENCRIPTAR LA CONTRASÑA DEL USUARIO
def encriptar_contrasena(password: str):
    return pwd_context.hash(password)


# PARA LA VERIFICACIÓN DE DICHA CONTRASEÑA
def verificar_contrasena(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


# CREO EL TOKEN DE SEGURIDAD
def crear_token(datos: dict, expires_delta: timedelta = None):
    to_encode = datos.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#SE VERIFICA DICHO TOKEN
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None