from sqlalchemy.orm import Session
import obrigacao_acessoria_repository
import schemas
from fastapi import HTTPException

def create_obrigacao_acessoria(db: Session, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    return obrigacao_acessoria_repository.create_obrigacao_acessoria(db, obrigacao)

def get_obrigacoes_acessorias(db: Session):
    return obrigacao_acessoria_repository.get_obrigacoes_acessorias(db)

def get_obrigacao_acessoria(db: Session, obrigacao_id: int):
    obrigacao = obrigacao_acessoria_repository.get_obrigacao_acessoria(db, obrigacao_id)
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    return obrigacao

def update_obrigacao_acessoria(db: Session, obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaBase):
    db_obrigacao = obrigacao_acessoria_repository.update_obrigacao_acessoria(db, obrigacao_id, obrigacao)
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    return db_obrigacao

def delete_obrigacao_acessoria(db: Session, obrigacao_id: int):
    sucesso = obrigacao_acessoria_repository.delete_obrigacao_acessoria(db, obrigacao_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    return {"message": "Obrigação acessória excluída com sucesso"}
