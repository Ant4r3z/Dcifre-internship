from sqlalchemy.orm import Session
import empresa_repository
import schemas
from fastapi import HTTPException

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    try:
        empresa_criada = empresa_repository.create_empresa(db, empresa)
        return empresa_criada  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar empresa no banco de dados")

def get_empresas(db: Session):
    try:
        return empresa_repository.get_empresas(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar empresas no banco de dados")

def get_empresa(db: Session, empresa_id: int):
    try:
        empresa = empresa_repository.get_empresa(db, empresa_id)
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        return empresa  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar a empresa com ID {empresa_id}")

def update_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaUpdate):
    try:
        db_empresa = empresa_repository.update_empresa(db, empresa_id, empresa)
        if not db_empresa:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        return db_empresa  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar empresa com ID {empresa_id}")

def delete_empresa(db: Session, empresa_id: int):
    try:
        sucesso = empresa_repository.delete_empresa(db, empresa_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        return {"message": "Empresa excluída com sucesso"}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir empresa com ID {empresa_id}")
