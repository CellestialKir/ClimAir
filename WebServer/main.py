from contextlib import asynccontextmanager
from api.dataTransfer import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.data_broker import broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.stop()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

#
# @app.on_event("startup")
# async def start_broker():
#     await broker.start()
#
# @app.on_event("shutdown")
# async def stop_broker():
#     await broker.close()





