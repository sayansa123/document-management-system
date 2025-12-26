from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import FileResponse 
from sqlalchemy.orm import Session

from typing import Literal
from sqlalchemy import text

from database.mysql.database import get_db
from database.mysql.models import Files


import os


router = APIRouter()

# download file api
@router.get('/document/download/{id}')
def download(
    id : int = Path(..., ge=1),
    db : Session = Depends(get_db)
):
    existing_file = db.query(Files).filter(Files.id == id).first()
    if not existing_file:
        raise HTTPException(status_code=404, detail='Item not found')
    if existing_file.is_deleted == True:
        raise HTTPException(status_code=400, detail='Item not found')
    backend_file_directory = 'uploads'
    backend_path = os.path.join(backend_file_directory, existing_file.file_name)
    if not os.path.isfile(backend_path):
        raise HTTPException(status_code=404, detail='Item not found')


    return FileResponse(
        path=backend_path,
        filename=existing_file.file_name
    )