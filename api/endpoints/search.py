from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.mysql.database import get_db, Base, engine
from database.mysql.models import Files

from datetime import datetime
from database.mongodb.configuration import mongo_db_collection
from services.mongodb_service import retrieve_individual2


router = APIRouter()


# retrive data from sql & mongodb


# Searching and Filtering
# only PDFs, only images
# search by filename
# filter by date [uploaded_at between two dates]
# filter by size [file_size > 1MB]
@router.get('/document/searching_Filtering')
def searching_Filtering(
    file_type : str = Query(description='MIME TYPE of the file', example='application/pdf', default=None),
    file_name : str = Query(description='Name of the file', example='Dwaipayan_Sardar_Resume.pdf', default=None),
    min_size : int = Query(description='In MB', example='1', default=None),
    max_size : int = Query(description='In MB', example='4', default=None),
    start_date : datetime = Query(description='Starting Date', example='2014-11-23',default=None),
    end_date : datetime = Query(description='Ending Date', example='2025-12-31',default=None),
    tag : str = Query(description='Tags of the file', example='cv', default=None),
    db : Session = Depends(get_db)
):
    # General = db.query(Files).filter(X).filter(Y).filter(Z).all()
    
    # query = db.query(Files)
    query = db.query(Files)

    # query = query.filter(...)
    if start_date and end_date:
        query = query.filter(Files.uploaded_at.between(start_date, end_date))
    elif start_date:
        query = query.filter(Files.uploaded_at >= start_date)
    elif end_date:
        query = query.filter(Files.uploaded_at <= end_date)
    
    if max_size and min_size:
        query = query.filter(Files.file_size.between(min_size, max_size))
    elif max_size:
        query = query.filter(Files.file_size < max_size)
    elif min_size:
        query = query.filter(Files.file_size > min_size)
    
    if file_type:
        query = query.filter(Files.file_type == file_type)

    if file_name:
        query = query.filter(Files.file_name.contains(file_name))

    # existing_files_sql = query.all()
    existing_files_sql = query.all()

    # merging with mongodb with filtering tags
    existing_files_mongodb_iterator = mongo_db_collection.find()
    existing_files_mongodb = [retrieve_individual2(i, tag) for i in existing_files_mongodb_iterator]
    existing_files_mongodb_lookup_table = {i['file_id']:i for i in existing_files_mongodb if i is not None}
    merge = [{
            'id' : i.id,
            'file_name' : i.file_name,
            'file_path' : i.file_path,
            'file_size' : i.file_size,
            'file_type' : i.file_type,
            'uploaded_at' : i.uploaded_at,
            'mongo':{
                'description' : existing_files_mongodb_lookup_table.get(i.id,{}).get('description'),
                'tags':existing_files_mongodb_lookup_table.get(i.id,{}).get('tags')
            }
        }for i in existing_files_sql if i.is_deleted==False and i.id in existing_files_mongodb_lookup_table]
    return merge