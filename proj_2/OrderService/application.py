import uvicorn 
from fastapi import FastAPI
from container import Container
import endpoints
from database import database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

def create_app():
    container = Container()
    container.wire(modules=[endpoints])
    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(endpoints.router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run('application:app', host='0.0.0.0', port=8000, reload=True)