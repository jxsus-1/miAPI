import logging
from fastapi import HTTPException
from bson import ObjectId

from models.product import Product
from utils.mongodb import get_collection

logger = logging.getLogger(__name__)

async def create_product(product: Product) -> Product:
    try:
        coll = get_collection("products")

        new_product = Product(
            name=product.name,
            price=product.price,
            category_id=product.category_id
        )

        product_dict = new_product.model_dump(exclude={"product_id"})
        inserted = coll.insert_one(product_dict)
        new_product.product_id = str(inserted.inserted_id)
        return new_product

    except Exception as e:
        logger.error(f"Error creando producto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creando producto en la base de datos")


async def get_product(product_id: str) -> Product:
    try:
        coll = get_collection("products")
        product_data = coll.find_one({"_id": ObjectId(product_id)})
        if not product_data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        product_data["product_id"] = str(product_data["_id"])
        return Product.model_validate(product_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo producto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error consultando producto en la base de datos")


async def update_product(product_id: str, product: Product) -> Product:
    try:
        coll = get_collection("products")
        update_result = coll.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product.model_dump(exclude={"product_id"})}
        )
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado para actualizar")

        product.product_id = product_id
        return product

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando producto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando producto en la base de datos")


async def delete_product(product_id: str) -> dict:
    try:
        coll = get_collection("products")
        delete_result = coll.delete_one({"_id": ObjectId(product_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado para eliminar")

        return {"message": "Producto eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando producto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error eliminando producto en la base de datos")
