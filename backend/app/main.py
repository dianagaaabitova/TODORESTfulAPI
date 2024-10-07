import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from api.routers import api_router
from database.db_helper import db_helper
from database.models import Base

app = FastAPI()
app.include_router(api_router)

def setup_logging():
    log_level = logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    setup_logging()

    yield

app = FastAPI(lifespan=lifespan, root_path="/api", title="TODORESTFulAPI")

app.include_router(api_router)
Instrumentator().instrument(app).expose(app)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
