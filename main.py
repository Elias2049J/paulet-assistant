from fastapi import FastAPI
from api.routes import server

app = FastAPI()
app.include_router(server.router)
