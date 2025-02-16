from pydantic import BaseModel, EmailStr
from typing import List, Optional
import enum

# Esquemas de Obrigação Acessoria
class PeriodicidadeEnum(str, enum.Enum):
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: PeriodicidadeEnum

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoriaUpdate(BaseModel):
    nome: Optional[str] = None
    periodicidade: PeriodicidadeEnum

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int


# Esquemas de Empresa
class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    endereco: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

class Empresa(EmpresaBase):
    id: int
    obrigacoes: List[ObrigacaoAcessoria] = []
