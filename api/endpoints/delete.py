from fastapi import APIRouter, Depends, Path, HTTPException

from sqlalchemy.orm import Session

from typing import Literal
from sqlalchemy import text

from database.mysql.database import get_db
from database.mysql.models import Files


from database.mongodb.configuration import mongo_db_collection

import os
import shutil

router = APIRouter()


# delete file (flow == 1.Disk -> 2.Mongo Db -> 3.MySql)
@router.delete('/document/delete/{id}')
def soft_delete(
    id : int = Path(ge=1),
    db : Session = Depends(get_db)
):
    # exist on sql or sql_is_delete == True/False
    exists_in_sql = db.query(Files).filter(Files.id == id).first()
    if not exists_in_sql or (exists_in_sql.is_deleted == True):
        raise HTTPException(status_code=404, detail='Item not found')
    
    exists_in_sql.is_deleted = True
    db.commit()
    db.refresh(exists_in_sql)

    # rename the file from locak disks
    directory = 'uploads'
    path = os.path.join(directory, exists_in_sql.file_name)
    name, ext = os.path.splitext(exists_in_sql.file_name)

    new_name = f'{name}_deleted{ext}'
    new_path = os.path.join(directory, new_name)
    os.rename(path, new_path)

    return exists_in_sql





# clean (Reset) entire table and collection with local files
@router.delete('/files/hard_delete')
def hard_delete(
    select_db:Literal['mysql','mongodb','local_files'],
    sql : Session = Depends(get_db)
):
    if select_db == 'mongodb':
        mongo_db_collection.delete_many({})
    elif select_db =='mysql':
        sql.execute(text('DROP TABLE IF EXISTS files'))
    elif select_db=='local_files':
        folder = 'uploads'
        shutil.rmtree(folder)

    return 'delete successfully'
