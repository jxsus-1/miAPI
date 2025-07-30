from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.category import Category, CategoryCreate, CategoryUpdate
from controllers.controller_category import (
    create_category,
    get_category_by_id,
    list_categories,
    update_category,
    delete_category
)
from utils.security import validateadmin

router = APIRouter(prefix="/categories", tags=["📂 Categories"])

@router.post("/", response_model=Category)
@validateadmin
async def create_category_endpoint(request: Request, category_data: CategoryCreate) -> Category:
    """Crear una nueva categoría (requiere permisos de admin)"""
    return await create_category(category_data)

@router.get("/", response_model=List[Category])
async def list_categories_endpoint() -> List[Category]:
    """Listar todas las categorías"""
    return await list_categories()

@router.get("/{category_id}", response_model=Category)
async def get_category_by_id_endpoint(category_id: str) -> Category:
    """Obtener una categoría por ID"""
    category = await get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.put("/{category_id}", response_model=Category)
@validateadmin
async def update_category_endpoint(category_id: str, category_data: CategoryUpdate) -> Category:
    """Actualizar una categoría (requiere permisos de admin)"""
    updated = await update_category(category_id, category_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return updated

@router.delete("/{category_id}")
@validateadmin
async def delete_category_endpoint(category_id: str) -> dict:
    """Eliminar una categoría (requiere permisos de admin)"""
    deleted = await delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada correctamente"}
