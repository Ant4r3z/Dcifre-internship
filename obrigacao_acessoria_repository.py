from sqlalchemy.orm import Session
import models, schemas

def create_obrigacao_acessoria(db: Session, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

def get_obrigacoes_acessorias(db: Session):
    return db.query(models.ObrigacaoAcessoria).all()

def get_obrigacao_acessoria(db: Session, obrigacao_id: int):
    return db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()

def update_obrigacao_acessoria(db: Session, obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaBase):
    db_obrigacao = get_obrigacao_acessoria(db, obrigacao_id)
    if not db_obrigacao:
        return None

    for key, value in obrigacao.model_dump(exclude_unset=True).items():
        setattr(db_obrigacao, key, value)

    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

def delete_obrigacao_acessoria(db: Session, obrigacao_id: int):
    db_obrigacao = get_obrigacao_acessoria(db, obrigacao_id)
    if not db_obrigacao:
        return None

    db.delete(db_obrigacao)
    db.commit()
    return True
