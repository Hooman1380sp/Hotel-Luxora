from fastapi import FastAPI
import uvicorn

# from routers. import router as users

app = FastAPI(
    
)
# app.include_router(users, tags=["user"], prefix="/users")


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)