from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.product import Product, ProductCreate, ProductUpdate
from controllers.controller_product import (
    create_product,
    get_product_by_id,
    list_products,
    update_product,
    delete_product
)
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/products", tags=["📦 Products"])

@router.post("/", response_model=Product)
@validateadmin
async def create_product_endpoint(request: Request, product_data: ProductCreate) -> Product:
    """Crear un nuevo producto (requiere permisos de admin)"""
    return await create_product(product_data)

@router.get("/", response_model=List[Product])
async def list_products_endpoint() -> List[Product]:
    """Listar todos los productos"""
    return await list_products()

@router.get("/{product_id}", response_model=Product)
async def get_product_by_id_endpoint(product_id: str) -> Product:
    """Obtener un producto por ID"""
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.put("/{product_id}", response_model=Product)
@validateadmin
async def update_product_endpoint(product_id: str, product_data: ProductUpdate) -> Product:
    """Actualizar un producto (requiere permisos de admin)"""
    updated = await update_product(product_id, product_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@router.delete("/{product_id}")
@validateadmin
async def delete_product_endpoint(product_id: str) -> dict:
    """Eliminar un producto (requiere permisos de admin)"""
    deleted = await delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
