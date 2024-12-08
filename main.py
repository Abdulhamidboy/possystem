from fastapi import FastAPI
from src.api import router  
import uvicorn

fapp = FastAPI()  


fapp.include_router(router)

@fapp.get("/")
def read_root():
    return {"message": "POS System Backend"}

if __name__ == '__main__':
    uvicorn.run("main:fapp", reload=True)
