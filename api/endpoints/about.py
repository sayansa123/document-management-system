from fastapi import APIRouter

router = APIRouter()

# endpoint -> about 
@router.get('/docmanager/about')
def about():
    return {
        '💡 What this project is A backend system where:':{
            1:'Users upload files (PDF, images, CSV)',
            2:'Metadata goes to MySQL',
            3:'File + flexible data goes to MongoDB',
            4:'Files are stored on disk (or cloud later)',
            5:'Admin can analyze uploads'
        }
    }