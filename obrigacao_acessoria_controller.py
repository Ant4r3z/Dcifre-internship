from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
import obrigacao_acessoria_service

router = APIRouter(prefix="/obrigacoes", tags=["Obrigação Acessória"])

@router.post("/", response_model=schemas.ObrigacaoAcessoria)
def create_obrigacao_acessoria(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    return obrigacao_acessoria_service.create_obrigacao_acessoria(db, obrigacao)

@router.get("/", response_model=list[schemas.ObrigacaoAcessoria])
def get_obrigacoes_acessorias(db: Session = Depends(get_db)):
    return obrigacao_acessoria_service.get_obrigacoes_acessorias(db)

@router.get("/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def get_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    return obrigacao_acessoria_service.get_obrigacao_acessoria(db, obrigacao_id)

@router.put("/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def update_obrigacao_acessoria(obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaBase, db: Session = Depends(get_db)):
    return obrigacao_acessoria_service.update_obrigacao_acessoria(db, obrigacao_id, obrigacao)

@router.delete("/{obrigacao_id}")
def delete_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    return obrigacao_acessoria_service.delete_obrigacao_acessoria(db, obrigacao_id)
