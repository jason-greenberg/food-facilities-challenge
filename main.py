from fastapi import FastAPI

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
