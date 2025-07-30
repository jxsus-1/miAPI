from pydantic import BaseModel, Field
from typing import Optional

class Catalog(BaseModel):
    catalog_id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    product_id: str = Field(
        description="Referencia al producto",
        examples=["64bfe234c9e12ab3456def78"]
    )

    name: str = Field(
        description="Nombre del producto",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9' -]+$",
        examples=["Smartphone XYZ", "Cafetera 123"]
    )

    availability: bool = Field(
        default=True,
        description="Disponibilidad del producto en la tienda (con stock o sin stock)"
    )
