from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS IMPORT
from database.mysql.database import Base, engine

from api.endpoints.upload import router as uploading
from api.endpoints.delete import router as deleting
from api.endpoints.download import router as downloading
from api.endpoints.search import router as searching
from api.endpoints.retrival import router as retrivaling
from api.endpoints.about import router as about

app = FastAPI()

# ========== ADD THIS CORS CONFIGURATION ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =================================================

@app.get("/")
def root():
    return {"message": "More to see the about section"}

# metadata of the table
Base.metadata.create_all(bind = engine)

# include router
app.include_router(about)
app.include_router(uploading)
app.include_router(deleting)
app.include_router(downloading)
app.include_router(searching)
app.include_router(retrivaling)
