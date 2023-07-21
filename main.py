from fastapi import FastAPI

from db.db_setup import engine

app = FastAPI(
    title="Food Facilities Challenge API",
    version="0.1.0",
    description="API for Food Facilities Challenge",
    contact={
        "name": "Jason Greenberg",
        "email": "jasonrgreenberg@gmail.com",
        "url": "jasongreenberg.dev"
    },
    license_info={
        "name": "MIT License"
    }
)
