from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas
from database import get_db
import obrigacao_acessoria_service

router = APIRouter(prefix="/obrigacoes", tags=["Obrigação Acessória"])

@router.post("/", response_model=schemas.ObrigacaoAcessoria, status_code=status.HTTP_201_CREATED)
def create_obrigacao_acessoria(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    try:
        return obrigacao_acessoria_service.create_obrigacao_acessoria(db, obrigacao)
    except HTTPException as e:
        raise e  

@router.get("/", response_model=list[schemas.ObrigacaoAcessoria])
def get_obrigacoes_acessorias(db: Session = Depends(get_db)):
    try:
        return obrigacao_acessoria_service.get_obrigacoes_acessorias(db)
    except HTTPException as e:
        raise e  

@router.get("/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def get_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    try:
        return obrigacao_acessoria_service.get_obrigacao_acessoria(db, obrigacao_id)
    except HTTPException as e:
        raise e  

@router.put("/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria)
def update_obrigacao_acessoria(obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaBase, db: Session = Depends(get_db)):
    try:
        return obrigacao_acessoria_service.update_obrigacao_acessoria(db, obrigacao_id, obrigacao)
    except HTTPException as e:
        raise e  

@router.delete("/{obrigacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    try:
        return obrigacao_acessoria_service.delete_obrigacao_acessoria(db, obrigacao_id)
    except HTTPException as e:
        raise e  
