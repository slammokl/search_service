from datetime import date 

from pydantic import BaseModel, ConfigDict 

class DocumentOut(BaseModel): 
    id: int 
    text: str 
    rubrics: list[str] 
    created_date: date 

    model_config = ConfigDict(from_attributes=True) 

