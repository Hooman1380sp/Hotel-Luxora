from fastapi import FastAPI
import uvicorn
from settings import get_settings

# from routers. import router as users

app = FastAPI(

)


# app.include_router(users, tags=["user"], prefix="/users")

@app.on_event("startup")
async def startup_event():
    """ make index on email field at first step"""
    settings = get_settings()
    db = settings.mongo_db
    user_collection = db["User"]

    await user_collection.create_index("email", unique=True)


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
