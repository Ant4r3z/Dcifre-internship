from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import models, schemas

def create_obrigacao_acessoria(db: Session, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())
    db.add(db_obrigacao)
    try:
        db.commit()
        db.refresh(db_obrigacao)
        return db_obrigacao
    except IntegrityError as e:
        db.rollback()  # Desfaz a transação em caso de erro de integridade
        raise IntegrityError("Erro de integridade: Dados duplicados ou inválidos") from e
    except SQLAlchemyError as e:
        db.rollback()  # Rollback em caso de erro genérico do SQLAlchemy
        raise SQLAlchemyError("Erro ao criar obrigação acessória no banco de dados") from e

def get_obrigacoes_acessorias(db: Session):
    try:
        return db.query(models.ObrigacaoAcessoria).all()
    except SQLAlchemyError as e:
        raise SQLAlchemyError("Erro ao buscar obrigações acessórias no banco de dados") from e

def get_obrigacao_acessoria(db: Session, obrigacao_id: int):
    try:
        return db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Erro ao buscar a obrigação acessória com ID {obrigacao_id} no banco de dados") from e

def update_obrigacao_acessoria(db: Session, obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaBase):
    db_obrigacao = get_obrigacao_acessoria(db, obrigacao_id)
    if not db_obrigacao:
        raise ValueError(f"Obrigação acessória com ID {obrigacao_id} não encontrada.")
    
    try:
        for key, value in obrigacao.model_dump(exclude_unset=True).items():
            setattr(db_obrigacao, key, value)

        db.commit()
        db.refresh(db_obrigacao)
        return db_obrigacao
    except IntegrityError as e:
        db.rollback()  
        raise IntegrityError("Erro de integridade ao atualizar obrigação acessória") from e
    except SQLAlchemyError as e:
        db.rollback()  
        raise SQLAlchemyError(f"Erro ao atualizar obrigação acessória com ID {obrigacao_id}") from e

def delete_obrigacao_acessoria(db: Session, obrigacao_id: int):
    db_obrigacao = get_obrigacao_acessoria(db, obrigacao_id)
    if not db_obrigacao:
        raise ValueError(f"Obrigação acessória com ID {obrigacao_id} não encontrada.")
    
    try:
        db.delete(db_obrigacao)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback() 
        raise SQLAlchemyError(f"Erro ao excluir obrigação acessória com ID {obrigacao_id}") from e
