# import(Base, datatypes) → Model/table Class → Model/table → Columns/Attributes

from database.mysql.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

class Files(Base):
    __tablename__ =  'files'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(100))
    file_path = Column(String(100))
    file_size = Column(Float)
    file_type = Column(String(100))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)