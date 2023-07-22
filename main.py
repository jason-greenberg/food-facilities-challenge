from fastapi import FastAPI
from api import users, locations, permits

from db.db_setup import engine
from db.models import user, location, permit

user.Base.metadata.create_all(bind=engine)
location.Base.metadata.create_all(bind=engine)
permit.Base.metadata.create_all(bind=engine)

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

app.include_router(users.router)
