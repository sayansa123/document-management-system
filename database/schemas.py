# schema = Blueprint/validation 

# both for sql & mongodb
from datetime import datetime
from pydantic import BaseModel, field_validator

import re

# For SQL
class Pydantic_Files_Create_SQL(BaseModel):
    file_name : str
    file_path : str
    file_size : float
    file_type : str
    # date time not needed here (it's default value is datetime.utcnow in models)

class Pydantic_Files_Response_SQL(Pydantic_Files_Create_SQL):
    id : int
    uploaded_at : datetime
    is_deleted : bool
    class Config:
        from_attributes = True


# For MongoDB
class Pydantic_Files_Storeing_MongoDB(BaseModel):
    file_id: int
    description: str
    tags: list[str]
    uploaded_at: datetime

    @field_validator('tags', mode='before')     # runs BEFORE normal Pydantic validation
    @classmethod
    def tag_field_validator(cls, value):
        # If input is a STRING --- Example: "cv,job"  --- split by comma, strip spaces
        if isinstance(value, str):
            value = [re.sub(r"[^a-zA-Z]",'',i.lower().strip()) for i in value.split(',') if re.sub(r"[^a-zA-Z]",'',i)] # value = value.strip().split(',')
    
        # If input is a LIST with ONE element --- Example: ["@   cv,job"]
        elif isinstance(value,list) and len(value)==1 and ',' in value[0]:
            value = [re.sub(r"[^a-zA-Z]",'',i.lower().strip()) for i in value[0].split(',') if re.sub(r"[^a-zA-Z]",'',i)]
        return value
