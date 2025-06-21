from fastapi import FastAPI
from database import create_db_and_tables
from routes import transacciones, usuarios, presupuestos

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()
    

app.include_router(transacciones.router)
app.include_router(usuarios.router)
app.include_router(presupuestos.router)