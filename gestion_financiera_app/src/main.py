from fastapi import FastAPI
from src.auth.router import auth_router
from src.roles.router import role_router
#from src.users.router import users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(role_router)

@app.get("/")
def root():
    return {"message": "API is up"}
