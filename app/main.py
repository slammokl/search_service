from contextlib import asynccontextmanager 

from fastapi import FastAPI 

from app.database import Base, engine 
from app.es_client import es, init_index 
from app.routes import router 

@asynccontextmanager 
async def lifespan(app: FastAPI): 
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 
    await init_index() 
    yield 
    await es.close() 
    await engine.dispose() 

app = FastAPI(
    title="Service for Posts search", 
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router) 

