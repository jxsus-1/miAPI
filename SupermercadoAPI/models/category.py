from pydantic import BaseModel, Field
from typing import Optional

class Category(BaseModel):
    category_id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    name: str = Field(
        description="Nombre de la categoría",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Electrónica", "Hogar y Cocina"]
    )
