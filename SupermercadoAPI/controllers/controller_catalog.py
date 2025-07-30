import logging
from fastapi import HTTPException
from bson import ObjectId

from models.catalog import Catalog
from utils.mongodb import get_collection

logger = logging.getLogger(__name__)

async def create_catalog(catalog: Catalog) -> Catalog:
    try:
        coll = get_collection("catalogs")

        new_catalog = Catalog(
            product_id=catalog.product_id,
            name=catalog.name,
            availability=catalog.availability
        )

        catalog_dict = new_catalog.model_dump(exclude={"catalog_id"})
        inserted = coll.insert_one(catalog_dict)
        new_catalog.catalog_id = str(inserted.inserted_id)
        return new_catalog

    except Exception as e:
        logger.error(f"Error creando catálogo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creando catálogo en la base de datos")


async def get_catalog(catalog_id: str) -> Catalog:
    try:
        coll = get_collection("catalogs")
        catalog_data = coll.find_one({"_id": ObjectId(catalog_id)})
        if not catalog_data:
            raise HTTPException(status_code=404, detail="Catálogo no encontrado")

        catalog_data["catalog_id"] = str(catalog_data["_id"])
        return Catalog.model_validate(catalog_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo catálogo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error consultando catálogo en la base de datos")


async def update_catalog(catalog_id: str, catalog: Catalog) -> Catalog:
    try:
        coll = get_collection("catalogs")
        update_result = coll.update_one(
            {"_id": ObjectId(catalog_id)},
            {"$set": catalog.model_dump(exclude={"catalog_id"})}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Catálogo no encontrado para actualizar")

        catalog.catalog_id = catalog_id
        return catalog

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando catálogo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando catálogo en la base de datos")


async def delete_catalog(catalog_id: str) -> dict:
    try:
        coll = get_collection("catalogs")
        delete_result = coll.delete_one({"_id": ObjectId(catalog_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Catálogo no encontrado para eliminar")

        return {"message": "Catálogo eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando catálogo: {str(e)}")
        raise HTTPException(status_code=500, detail="Error eliminando catálogo en la base de datos")
