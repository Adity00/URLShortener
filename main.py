from fastapi import FastAPI

from routes.urls import router

app = FastAPI()

@app.get("/")
def home():
    return{
        "message":"Welcome to URL shortener"
    }

@app.get("/about")
def about():
    return{
        "Project":"URL shortener",
        "Author":"Adi"
    }

app.include_router(router)
