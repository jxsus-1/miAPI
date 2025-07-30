from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Product(BaseModel):
    product_id: Optional[str] = Field(
        default=None,
        description="MongoDB ID del producto, generado automáticamente"
    )

    name: str = Field(
        description="Nombre del producto",
        min_length=2,
        max_length=100,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9' -]+$",
        examples=["Camiseta Deportiva", "Zapatos de cuero"]
    )

    price: float = Field(
        ge=0,
        description="Precio unitario del producto. No puede ser negativo.",
        examples=[199.99]
    )

    category_id: str = Field(
        description="ID de la categoría a la que pertenece el producto",
        examples=["64c70c2b1f34c42c7a3b77d8"]
    )

    @field_validator('price')
    @classmethod
    def validate_price_format(cls, value: float):
        # Asegura que el precio tenga máximo dos decimales
        if not re.match(r'^\d+(\.\d{1,2})?$', str(value)):
            raise ValueError("El precio debe tener como máximo dos decimales.")
        return value
