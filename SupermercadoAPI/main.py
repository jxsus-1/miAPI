import uvicorn
import logging

from fastapi import FastAPI, Request

from controllers.controller_user import create_user, login

from models.user import User
from models.login import Login

from utils.security import validateuser, validateadmin


app = FastAPI(
    title="API REST - Tienda",
    description="Sistema de gestión: users, products, category, inventory, catálog y order",
    version="1.0.0"
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API REST de la Tienda", "version": "0.0.0"}

@app.post("/users", response_model=User)
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)

@app.get("/exampleadmin")
@validateadmin
async def example_admin(request: Request):
    return {
        "message": "Este es un endpoint de ejemplo para admin.",
        "admin": request.state.admin
    }

@app.get("/exampleuser")
@validateuser
async def example_user(request: Request):
    return {
        "message": "Este es un endpoint de ejemplo para usuario.",
        "email": request.state.email
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
