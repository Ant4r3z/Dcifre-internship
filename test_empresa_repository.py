import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Empresa
from schemas import EmpresaCreate, EmpresaUpdate
from empresa_repository import create_empresa, get_empresas, get_empresa, update_empresa, delete_empresa

# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Criação do motor de banco de dados e da sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação do banco de dados a cada teste
@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.create_all(bind=engine)  # Cria as tabelas
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após o teste

# Teste para criar uma empresa
def test_create_empresa(setup_db):
    db = setup_db
    empresa_data = EmpresaCreate(
        nome="Empresa Teste",
        cnpj="12345678000195",
        endereco="Rua Teste, 123",
        email="teste@empresa.com",
        telefone="123456789"
    )
    
    empresa = create_empresa(db, empresa_data)
    
    assert empresa.id is not None
    assert empresa.nome == "Empresa Teste"
    assert empresa.cnpj == "12345678000195"
    assert empresa.endereco == "Rua Teste, 123"
    assert empresa.email == "teste@empresa.com"
    assert empresa.telefone == "123456789"

# Função de teste para buscar todas as empresas
def test_get_empresas(setup_db):
    db = setup_db
    empresa_data = EmpresaCreate(
        nome="Empresa Teste 2",
        cnpj="98765432000199",
        endereco="Rua Teste 2, 456",
        email="teste2@empresa.com",
        telefone="987654321"
    )
    
    create_empresa(db, empresa_data)
    
    empresas = get_empresas(db)
    assert len(empresas) > 0
    assert empresas[0].nome == "Empresa Teste 2"

# Função de teste para buscar uma empresa por ID
def test_get_empresa(setup_db):
    db = setup_db
    empresa_data = EmpresaCreate(
        nome="Empresa Teste 3",
        cnpj="13579246800100",
        endereco="Rua Teste 3, 789",
        email="teste3@empresa.com",
        telefone="135792468"
    )
    
    empresa = create_empresa(db, empresa_data)
    empresa_fetched = get_empresa(db, empresa.id)
    
    assert empresa_fetched is not None
    assert empresa_fetched.id == empresa.id
    assert empresa_fetched.nome == "Empresa Teste 3"

# Função de teste para atualizar uma empresa
def test_update_empresa(setup_db):
    db = setup_db
    empresa_data = EmpresaCreate(
        nome="Empresa Teste 4",
        cnpj="24681357000111",
        endereco="Rua Teste 4, 321",
        email="teste4@empresa.com",
        telefone="246813579"
    )
    
    empresa = create_empresa(db, empresa_data)
    
    empresa_update_data = EmpresaUpdate(nome="Empresa Teste Atualizada", telefone="000000000")
    updated_empresa = update_empresa(db, empresa.id, empresa_update_data)
    
    assert updated_empresa is not None
    assert updated_empresa.nome == "Empresa Teste Atualizada"
    assert updated_empresa.telefone == "000000000"

# Função de teste para deletar uma empresa
def test_delete_empresa(setup_db):
    db = setup_db
    empresa_data = EmpresaCreate(
        nome="Empresa Teste 5",
        cnpj="10203040500055",
        endereco="Rua Teste 5, 654",
        email="teste5@empresa.com",
        telefone="102030405"
    )
    
    empresa = create_empresa(db, empresa_data)
    result = delete_empresa(db, empresa.id)
    
    assert result is True
    empresa_deleted = get_empresa(db, empresa.id)
    assert empresa_deleted is None
