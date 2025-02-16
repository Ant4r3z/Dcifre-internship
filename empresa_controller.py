from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
import empresa_service

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.post("/", response_model=schemas.Empresa)
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    return empresa_service.create_empresa(db, empresa)

@router.get("/", response_model=list[schemas.Empresa])
def get_empresas(db: Session = Depends(get_db)):
    return empresa_service.get_empresas(db)

@router.get("/{empresa_id}", response_model=schemas.Empresa)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    return empresa_service.get_empresa(db, empresa_id)

@router.put("/{empresa_id}", response_model=schemas.Empresa)
def update_empresa(empresa_id: int, empresa: schemas.EmpresaUpdate, db: Session = Depends(get_db)):
    return empresa_service.update_empresa(db, empresa_id, empresa)

@router.delete("/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    return empresa_service.delete_empresa(db, empresa_id)
