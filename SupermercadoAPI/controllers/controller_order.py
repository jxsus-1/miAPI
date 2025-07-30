import logging
from fastapi import HTTPException
from typing import List
from bson import ObjectId

from models.order import Order
from utils.mongodb import get_collection

logger = logging.getLogger(__name__)

async def create_order(order: Order) -> Order:
    try:
        coll = get_collection("orders")

        new_order = Order(
            user_id=order.user_id,
            inventory_id=order.inventory_id,
            total=order.total
        )

        order_dict = new_order.model_dump(exclude={"order_id"})
        inserted = coll.insert_one(order_dict)
        new_order.order_id = str(inserted.inserted_id)
        return new_order

    except Exception as e:
        logger.error(f"Error creando orden: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creando orden en la base de datos")


async def get_order(order_id: str) -> Order:
    try:
        coll = get_collection("orders")
        order_data = coll.find_one({"_id": ObjectId(order_id)})
        if not order_data:
            raise HTTPException(status_code=404, detail="Orden no encontrada")

        order_data["order_id"] = str(order_data["_id"])
        return Order.model_validate(order_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo orden: {str(e)}")
        raise HTTPException(status_code=500, detail="Error consultando orden en la base de datos")


async def update_order(order_id: str, order: Order) -> Order:
    try:
        coll = get_collection("orders")
        update_result = coll.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": order.model_dump(exclude={"order_id"})}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Orden no encontrada para actualizar")

        order.order_id = order_id
        return order

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando orden: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando orden en la base de datos")


async def delete_order(order_id: str) -> dict:
    try:
        coll = get_collection("orders")
        delete_result = coll.delete_one({"_id": ObjectId(order_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Orden no encontrada para eliminar")

        return {"message": "Orden eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando orden: {str(e)}")
        raise HTTPException(status_code=500, detail="Error eliminando orden en la base de datos")
