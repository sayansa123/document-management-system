# URL → create Engine → make Session → declare Base class → providing session (get_db)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# mysql+pymysql://username:password@localhost:3306/database_name
DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/document_manager'

# database connection
engine = create_engine(DATABASE_URL)

# create session from get_db
Session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# parent of models/tables
Base = declarative_base()

# providing session
def get_db():
    db = Session_local()
    try:
        return db
    except:
        db.close()