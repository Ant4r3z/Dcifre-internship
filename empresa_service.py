from sqlalchemy.orm import Session
import empresa_repository
import schemas
from fastapi import HTTPException

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    return empresa_repository.create_empresa(db, empresa)

def get_empresas(db: Session):
    return empresa_repository.get_empresas(db)

def get_empresa(db: Session, empresa_id: int):
    empresa = empresa_repository.get_empresa(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

def update_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaUpdate):
    db_empresa = empresa_repository.update_empresa(db, empresa_id, empresa)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

def delete_empresa(db: Session, empresa_id: int):
    sucesso = empresa_repository.delete_empresa(db, empresa_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return {"message": "Empresa excluída com sucesso"}
