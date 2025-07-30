from fastapi import APIRouter, HTTPException, Request
from typing import List
from models.order import Order, CreateOrder, ChangeOrderStatus
from controllers.controller_order import (
    create_order,
    get_orders,
    get_order_by_id,
    update_order_status,
    delete_order
)
from utils.security import validateuser, validateadmin

router = APIRouter(prefix="/orders", tags=["📦 Orders"])

@router.post("/", response_model=Order)
@validateuser
async def create_order_endpoint(request: Request, order_data: CreateOrder) -> Order:
    """Crear una nueva orden (requiere estar autenticado)"""
    return await create_order(order_data)

@router.get("/", response_model=List[Order])
@validateadmin
async def list_orders_endpoint() -> List[Order]:
    """Listar todas las órdenes (requiere permisos de admin)"""
    return await get_orders()

@router.get("/{order_id}", response_model=Order)
@validateuser
async def get_order_by_id_endpoint(order_id: str) -> Order:
    """Obtener detalles de una orden por ID (requiere estar autenticado)"""
    order = await get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@router.put("/{order_id}/status", response_model=Order)
@validateadmin
async def update_order_status_endpoint(order_id: str, status_data: ChangeOrderStatus) -> Order:
    """Actualizar el estado de una orden (requiere permisos de admin)"""
    updated = await update_order_status(order_id, status_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return updated

@router.delete("/{order_id}")
@validateadmin
async def delete_order_endpoint(order_id: str) -> dict:
    """Eliminar una orden (requiere permisos de admin)"""
    deleted = await delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"message": "Orden eliminada correctamente"}
