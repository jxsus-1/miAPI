import logging
from fastapi import HTTPException
from typing import Optional
from bson import ObjectId

from models.inventory import Inventory
from utils.mongodb import get_collection

logger = logging.getLogger(__name__)

async def create_inventory(inventory: Inventory) -> Inventory:
    try:
        coll = get_collection("inventories")

        new_inventory = Inventory(
            product_id=inventory.product_id,
            stock=inventory.stock,
            date_in=inventory.date_in,
            date_out=inventory.date_out
        )

        inventory_dict = new_inventory.model_dump(exclude={"inventory_id"})
        inserted = coll.insert_one(inventory_dict)
        new_inventory.inventory_id = str(inserted.inserted_id)
        return new_inventory

    except Exception as e:
        logger.error(f"Error creando inventario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creando inventario en la base de datos")


async def get_inventory(inventory_id: str) -> Inventory:
    try:
        coll = get_collection("inventories")
        inventory_data = coll.find_one({"_id": ObjectId(inventory_id)})
        if not inventory_data:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        inventory_data["inventory_id"] = str(inventory_data["_id"])
        return Inventory.model_validate(inventory_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo inventario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error consultando inventario en la base de datos")


async def update_inventory(inventory_id: str, inventory: Inventory) -> Inventory:
    try:
        coll = get_collection("inventories")
        update_result = coll.update_one(
            {"_id": ObjectId(inventory_id)},
            {"$set": inventory.model_dump(exclude={"inventory_id"})}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Inventario no encontrado para actualizar")

        inventory.inventory_id = inventory_id
        return inventory

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando inventario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando inventario en la base de datos")


async def delete_inventory(inventory_id: str) -> dict:
    try:
        coll = get_collection("inventories")
        delete_result = coll.delete_one({"_id": ObjectId(inventory_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Inventario no encontrado para eliminar")

        return {"message": "Inventario eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando inventario: {str(e)}")
        raise HTTPException(status_code=500, detail="Error eliminando inventario en la base de datos")
