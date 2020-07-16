from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router

app = FastAPI()

origins = [
    "https://entroprise.com",
    "https://www.entroprise.com",
    "https://hasura.entroprise.com",
    "https://app.entroprise.com",
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
