from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import models, schemas

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    try:
        db_empresa = models.Empresa(**empresa.model_dump())
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError as e:
        db.rollback()  # Desfaz a transação em caso de erro de integridade (ex: violação de chave única)
        raise ValueError("Erro de integridade: Dados duplicados ou inválidos") from e
    except SQLAlchemyError as e:
        db.rollback()  # Rollback em caso de erro genérico do SQLAlchemy
        raise Exception("Erro ao criar empresa no banco de dados") from e

def get_empresas(db: Session):
    try:
        return db.query(models.Empresa).all()
    except SQLAlchemyError as e:
        raise Exception("Erro ao buscar empresas no banco de dados") from e

def get_empresa(db: Session, empresa_id: int):
    try:
        return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao buscar a empresa com ID {empresa_id} no banco de dados") from e

def update_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaUpdate):
    db_empresa = get_empresa(db, empresa_id)
    if not db_empresa:
        raise ValueError(f"Empresa com ID {empresa_id} não encontrada.")
    
    try:
        for key, value in empresa.model_dump(exclude_unset=True).items():
            setattr(db_empresa, key, value)
        
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError as e:
        db.rollback()  
        raise ValueError("Erro de integridade ao atualizar empresa") from e
    except SQLAlchemyError as e:
        db.rollback() 
        raise Exception(f"Erro ao atualizar empresa com ID {empresa_id}") from e

def delete_empresa(db: Session, empresa_id: int):
    db_empresa = get_empresa(db, empresa_id)
    if not db_empresa:
        raise ValueError(f"Empresa com ID {empresa_id} não encontrada.")
    
    try:
        db.delete(db_empresa)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Erro ao excluir empresa com ID {empresa_id}") from e
