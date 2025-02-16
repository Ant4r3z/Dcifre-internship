from sqlalchemy.orm import Session
import models, schemas

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def get_empresas(db: Session):
    return db.query(models.Empresa).all()

def get_empresa(db: Session, empresa_id: int):
    return db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

def update_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaUpdate):
    db_empresa = get_empresa(db, empresa_id)
    if not db_empresa:
        return None

    for key, value in empresa.model_dump(exclude_unset=True).items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def delete_empresa(db: Session, empresa_id: int):
    db_empresa = get_empresa(db, empresa_id)
    if not db_empresa:
        return None
    
    db.delete(db_empresa)
    db.commit()
    return True
