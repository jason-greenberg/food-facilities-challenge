from fastapi import FastAPI
from api import auth_routes, user_routes, permit_routes

from db.db_setup import engine
from db.models import user, permit

user.Base.metadata.create_all(bind=engine)
permit.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Facilities Challenge API",
    version="0.1.0",
    description="API for Food Facilities Challenge",
    contact={
        "name": "Jason Greenberg",
        "email": "jasonrgreenberg@gmail.com",
        "url": "https://jasongreenberg.dev"
    },
    license_info={
        "name": "MIT License"
    }
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router, prefix="/users")
app.include_router(permit_routes.router, prefix="/permits")
