from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.inventory import Inventory, InventoryCreate, InventoryUpdate
from controllers.controller_inventory import (
    create_inventory,
    get_inventory_by_id,
    list_inventory,
    update_inventory,
    delete_inventory
)
from utils.security import validateadmin

router = APIRouter(prefix="/inventory", tags=["📋 Inventory"])

@router.post("/", response_model=Inventory)
@validateadmin
async def create_inventory_endpoint(request: Request, inventory_data: InventoryCreate) -> Inventory:
    """Crear un nuevo registro de inventario (requiere permisos de admin)"""
    return await create_inventory(inventory_data)

@router.get("/", response_model=List[Inventory])
async def list_inventory_endpoint() -> List[Inventory]:
    """Listar todos los registros de inventario"""
    return await list_inventory()

@router.get("/{inventory_id}", response_model=Inventory)
async def get_inventory_by_id_endpoint(inventory_id: str) -> Inventory:
    """Obtener un registro de inventario por ID"""
    inv = await get_inventory_by_id(inventory_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inv

@router.put("/{inventory_id}", response_model=Inventory)
@validateadmin
async def update_inventory_endpoint(inventory_id: str, inventory_data: InventoryUpdate) -> Inventory:
    """Actualizar un registro de inventario (requiere permisos de admin)"""
    updated = await update_inventory(inventory_id, inventory_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return updated

@router.delete("/{inventory_id}")
@validateadmin
async def delete_inventory_endpoint(inventory_id: str) -> dict:
    """Eliminar un registro de inventario (requiere permisos de admin)"""
    deleted = await delete_inventory(inventory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return {"message": "Inventario eliminado correctamente"}
