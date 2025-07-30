from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Inventory(BaseModel):
    inventory_id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    product_id: str = Field(
        description="ID del producto al que pertenece este inventario",
        examples=["64bfe234c9e12ab3456def78"]
    )

    stock: int = Field(
        ge=0,
        description="Cantidad del producto disponible en almacén (stock ≥ 0)",
        examples=[100]
    )

    date_in: Optional[datetime] = Field(
        default=None,
        description="Fecha en que el producto ingresó al inventario",
        examples=["2025-07-30T15:30:00"]
    )

    date_out: Optional[datetime] = Field(
        default=None,
        description="Fecha en que el producto salió del inventario",
        examples=["2025-08-01T10:00:00"]
    )
