from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.db_setup import get_db
from pydantic_schemas.permit import PermitCreate, Permit
from api.utils.permits import (
    get_permits, create_permit, 
    get_permits_by_conditions
)
from api.auth.token import get_current_active_user

router = APIRouter()

@router.get("/", response_model=list[Permit])
async def read_permits(
    skip: int = 0, limit: int = 100, 
    applicant: str = None, status: str = None, 
    address: str = None, 
    latitude: float = None, longitude: float = None,
    db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    if applicant or address or (latitude and longitude):
        return get_permits_by_conditions(db=db, applicant=applicant, address=address, latitude=latitude, longitude=longitude, status=status, skip=skip, limit=limit)
    else:
        return get_permits(db=db, skip=skip, limit=limit)
        
@router.post("/", response_model=Permit, status_code=201)
async def create_new_permit(permit: PermitCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return create_permit(db=db, permit=permit)

