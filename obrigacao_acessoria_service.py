from sqlalchemy.orm import Session
import obrigacao_acessoria_repository
import schemas
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def create_obrigacao_acessoria(db: Session, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    try:
        return obrigacao_acessoria_repository.create_obrigacao_acessoria(db, obrigacao)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade: Dados duplicados ou inválidos"
        ) from e
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar obrigação acessória no banco de dados"
        ) from e

def get_obrigacoes_acessorias(db: Session):
    try:
        return obrigacao_acessoria_repository.get_obrigacoes_acessorias(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar obrigações acessórias no banco de dados"
        ) from e

def get_obrigacao_acessoria(db: Session, obrigacao_id: int):
    try:
        obrigacao = obrigacao_acessoria_repository.get_obrigacao_acessoria(db, obrigacao_id)
        if not obrigacao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada")
        return obrigacao
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar a obrigação acessória com ID {obrigacao_id}"
        ) from e

def update_obrigacao_acessoria(db: Session, obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaBase):
    try:
        db_obrigacao = obrigacao_acessoria_repository.update_obrigacao_acessoria(db, obrigacao_id, obrigacao)
        if not db_obrigacao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada")
        return db_obrigacao
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao atualizar obrigação acessória"
        ) from e
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar a obrigação acessória com ID {obrigacao_id}"
        ) from e

def delete_obrigacao_acessoria(db: Session, obrigacao_id: int):
    try:
        sucesso = obrigacao_acessoria_repository.delete_obrigacao_acessoria(db, obrigacao_id)
        if not sucesso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada")
        return {"message": "Obrigação acessória excluída com sucesso"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir a obrigação acessória com ID {obrigacao_id}"
        ) from e
