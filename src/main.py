from fastapi import FastAPI
import uvicorn

from models.router_menu import router as router_menu
from models.router_submeny import router as router_submenu
from models.router_dish import router as router_dish

app = FastAPI()

app.include_router(router_menu)

app.include_router(router_submenu)

app.include_router(router_dish)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000,  host="127.0.0.1", reload=True)
