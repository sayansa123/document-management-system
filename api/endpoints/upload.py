from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from database.mysql.database import get_db
from database.mysql.models import Files
from database.schemas import Pydantic_Files_Create_SQL

from database.schemas import Pydantic_Files_Storeing_MongoDB
from datetime import datetime
from database.mongodb.configuration import mongo_db_collection

import os


router = APIRouter()


# endpoint -> file upload & insert into db
@router.post('/document/upload')
def upload(
    files : UploadFile = File(...),
    description:str = Form(...),
    tags: list[str] = Form(...),
    db:Session = Depends(get_db),
):
    # 1. save file in upload folder
    file_name = files.filename

    uploaded_directory = 'uploads'
    os.makedirs(uploaded_directory, exist_ok=True)
    file_path = os.path.join(uploaded_directory, file_name)
    file_exists = os.path.exists(file_path)
    if file_exists:
        raise HTTPException(status_code=400, detail='File already exists')
    
    with open(file_path, 'wb') as f:
        data = files.file.read()
        f.write(data)
    

    # 2. Validate through pydantic  (For sql insertion)
    file_obj = Pydantic_Files_Create_SQL(
        file_name = files.filename,
        file_path = f'uploads/{files.filename}',
        file_size = files.size,
        file_type = files.content_type 
    )
    
    #convert pydantic obj -> dictionary
    dict = file_obj.model_dump()

    # sql obj
    new_file = Files(**dict)

    # inserting into data
    db.add(new_file)

    db.commit()
    db.refresh(new_file)


    # 3. Insert into MondoDb document
    mongo_db_full_obj = Pydantic_Files_Storeing_MongoDB(
        file_id = new_file.id,
        description = description,
        tags = tags,
        uploaded_at = datetime.utcnow()
    )

    #convert pydantic obj -> dictionary
    dict = mongo_db_full_obj.model_dump()

    response = mongo_db_collection.insert_one(dict)
    
    print(files)

    return {'message':f'document uploaded successfully: {new_file.file_name}'}