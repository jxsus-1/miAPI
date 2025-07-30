import logging
from fastapi import HTTPException
from bson import ObjectId

from models.category import Category
from utils.mongodb import get_collection

logger = logging.getLogger(__name__)

async def create_category(category: Category) -> Category:
    try:
        coll = get_collection("categories")

        new_category = Category(
            name=category.name
        )

        category_dict = new_category.model_dump(exclude={"category_id"})
        inserted = coll.insert_one(category_dict)
        new_category.category_id = str(inserted.inserted_id)
        return new_category

    except Exception as e:
        logger.error(f"Error creando categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creando categoría en la base de datos")


async def get_category(category_id: str) -> Category:
    try:
        coll = get_collection("categories")
        category_data = coll.find_one({"_id": ObjectId(category_id)})
        if not category_data:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

        category_data["category_id"] = str(category_data["_id"])
        return Category.model_validate(category_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error consultando categoría en la base de datos")


async def update_category(category_id: str, category: Category) -> Category:
    try:
        coll = get_collection("categories")
        update_result = coll.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": category.model_dump(exclude={"category_id"})}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Categoría no encontrada para actualizar")

        category.category_id = category_id
        return category

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando categoría en la base de datos")


async def delete_category(category_id: str) -> dict:
    try:
        coll = get_collection("categories")
        delete_result = coll.delete_one({"_id": ObjectId(category_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Categoría no encontrada para eliminar")

        return {"message": "Categoría eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando categoría: {str(e)}")
        raise HTTPException(status_code=500, detail="Error eliminando categoría en la base de datos")
