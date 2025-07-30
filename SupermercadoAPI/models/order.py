from pydantic import BaseModel, Field
from typing import Optional, List


class Order(BaseModel):
    order_id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    user_id: str = Field(
        description="ID de la persona que hizo la orden",
        examples=["64bfe234c9e12ab3456def78"]
    )

    inventory_id: List[str] = Field(
        description="Lista de IDs de productos en inventario asociados a la venta",
        examples=["64bfe234c9e12ab3456def78", "64bfe234c9e12ab3456def79"]
    )

    total: float = Field(
        ge=0,
        description="Total a pagar por la orden",
        examples=[1500.75]
    )
