from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.user import User, UserCreate, UserUpdate
from controllers.controller_user import (  
    create_user,
    get_user_by_id,
    list_users,
    update_user,
    delete_user
)
from utils.security import validateuser, validateadmin

router = APIRouter(prefix="/users", tags=["👤 Users"])

@router.post("/", response_model=User)
@validateadmin
async def create_user_endpoint(request: Request, user_data: UserCreate) -> User:
    """Crear un nuevo usuario (requiere permisos de admin)"""
    return await create_user(user_data)

@router.get("/", response_model=List[User])
@validateadmin
async def list_users_endpoint() -> List[User]:
    """Listar todos los usuarios (requiere permisos de admin)"""
    return await list_users()

@router.get("/{user_id}", response_model=User)
@validateuser
async def get_user_by_id_endpoint(user_id: str) -> User:
    """Obtener detalles de un usuario por su ID (requiere login)"""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=User)
@validateuser
async def update_user_endpoint(user_id: str, user_data: UserUpdate) -> User:
    """Actualizar datos de un usuario (requiere login)"""
    updated = await update_user(user_id, user_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated

@router.delete("/{user_id}")
@validateadmin
async def delete_user_endpoint(user_id: str) -> dict:
    """Eliminar un usuario (requiere permisos de admin)"""
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
