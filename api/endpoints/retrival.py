from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from database.mysql.database import get_db
from database.mysql.models import Files
from database.schemas import Pydantic_Files_Response_SQL

from database.mongodb.configuration import mongo_db_collection
from services.mongodb_service import retrieve_individual


router = APIRouter()



#####################################
@router.get('/document/retrival')
def retrival(
    page : int = Query(default=1, ge=1),
    limit : int = Query(default=50, ge=1),
    db : Session = Depends(get_db)
):
    start = (page-1)*limit
    end = start + limit
    mongodb_iterator = mongo_db_collection.find()
    existing_mongo_db = [retrieve_individual(i) for i in mongodb_iterator]
    existing_sql_db = db.query(Files).all()

    existing_mongo_db_dict = {i['file_id']:i for i in existing_mongo_db}
    
    final_merged_list = [{'id' :i.id ,
    'file_name' : i.file_name,
    'file_path' : i.file_path,
    'file_size' : i.file_size,
    'file_type' : i.file_type,
    'uploaded_at' : i.uploaded_at,
    'mongo' : {
        'description':existing_mongo_db_dict.get(i.id,{}).get('description'),
        'tags':existing_mongo_db_dict.get(i.id,{}).get('tags')
        }
    } for i in existing_sql_db if i.is_deleted==False]
    # http://localhost:8000/document/show/pagination/?page=2&limit=5

    return final_merged_list[start:end]









# endpoint -> Retrive from sql (Both Soft Deleted file and normal files)
@router.get('/document/sql_show', response_model=list[Pydantic_Files_Response_SQL])
def show(
    db:Session = Depends(get_db)
):
    return db.query(Files).all()







# endpoint -> Retrive from mongodb (Both files from SQL both Soft Deleted file and normal)
def retrieve_all(files):
    list = []
    for i in files:
        file_id = i['file_id']
        description = i['description']
        tags = i['tags']
        uploaded_at = i['uploaded_at']
        dict = {
            'file_id':file_id,
            'description':description,
            'tags':tags,
            'uploaded_at':uploaded_at
        }
        list.append(dict)
    return list
#####################################
@router.get('/document/mongo_db_show')
def show():
    files = mongo_db_collection.find()
    return retrieve_all(files)