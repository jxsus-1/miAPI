from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.catalog import Catalog, CatalogCreate, CatalogUpdate
from controllers.controller_catalog import (
    create_catalog,
    get_catalog_by_id,
    list_catalogs,
    update_catalog,
    delete_catalog
)
from utils.security import validateadmin

router = APIRouter(prefix="/catalog", tags=["🛍️ Catalog"])

@router.post("/", response_model=Catalog)
@validateadmin
async def create_catalog_endpoint(request: Request, catalog_data: CatalogCreate) -> Catalog:
    """Crear una nueva entrada en el catálogo (requiere permisos de admin)"""
    return await create_catalog(catalog_data)

@router.get("/", response_model=List[Catalog])
async def list_catalogs_endpoint() -> List[Catalog]:
    """Listar todos los productos en el catálogo"""
    return await list_catalogs()

@router.get("/{catalog_id}", response_model=Catalog)
async def get_catalog_by_id_endpoint(catalog_id: str) -> Catalog:
    """Obtener una entrada del catálogo por ID"""
    catalog = await get_catalog_by_id(catalog_id)
    if not catalog:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return catalog

@router.put("/{catalog_id}", response_model=Catalog)
@validateadmin
async def update_catalog_endpoint(catalog_id: str, catalog_data: CatalogUpdate) -> Catalog:
    """Actualizar una entrada del catálogo (requiere permisos de admin)"""
    updated = await update_catalog(catalog_id, catalog_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return updated

@router.delete("/{catalog_id}")
@validateadmin
async def delete_catalog_endpoint(catalog_id: str) -> dict:
    """Eliminar una entrada del catálogo (requiere permisos de admin)"""
    deleted = await delete_catalog(catalog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return {"message": "Catálogo eliminado correctamente"}
