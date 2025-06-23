from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    edad: int
    ingresos: int
    riesgo: str
    ocupacion: Optional[str] = None
    descripcion_personal: Optional[str] = None
    objetivo: Optional[str] = None
    horizonte_inversion: Optional[str] = None
    experiencia_inversion: Optional[str] = None
    intereses: Optional[List[str]] = []
