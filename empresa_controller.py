from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from database import get_db
import empresa_service

router = APIRouter(prefix="/empresas", tags=["Empresa"])

@router.post("/", response_model=schemas.Empresa, status_code=201)
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    try:
        return empresa_service.create_empresa(db, empresa)
    except HTTPException as e:
        raise e 

@router.get("/", response_model=list[schemas.Empresa])
def get_empresas(db: Session = Depends(get_db)):
    try:
        return empresa_service.get_empresas(db)
    except HTTPException as e:
        raise e 

@router.get("/{empresa_id}", response_model=schemas.Empresa)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    try:
        return empresa_service.get_empresa(db, empresa_id)
    except HTTPException as e:
        raise e 

@router.put("/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(empresa_id: int, empresa: schemas.EmpresaUpdate, db: Session = Depends(get_db)):
    try:
        return empresa_service.update_empresa(db, empresa_id, empresa)
    except HTTPException as e:
        raise e 

@router.delete("/{empresa_id}", status_code=204)
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    try:
        return empresa_service.delete_empresa(db, empresa_id)
    except HTTPException as e:
        raise e 
