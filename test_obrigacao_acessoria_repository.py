import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from schemas import EmpresaCreate, ObrigacaoAcessoriaCreate
from empresa_repository import create_empresa
from obrigacao_acessoria_repository import create_obrigacao_acessoria, get_obrigacao_acessoria, get_obrigacoes_acessorias, update_obrigacao_acessoria, delete_obrigacao_acessoria

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
    empresa_data = EmpresaCreate(
        nome="Empresa Teste",
        cnpj="12345678000195",
        endereco="Rua Teste, 123",
        email="teste@empresa.com",
        telefone="123456789"
    )
    empresa = create_empresa(db, empresa_data)
    yield db, empresa
    db.close()
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após o teste

# Teste para criar uma obrigacao acessoria
def test_create_obrigacao_acessoria(setup_db):
    db, empresa = setup_db

    obrigacao_data = ObrigacaoAcessoriaCreate(
        nome="Obrigações Teste",
        periodicidade="mensal",
        empresa_id=empresa.id
    )

    obrigacao = create_obrigacao_acessoria(db, obrigacao_data)

    assert obrigacao.id is not None
    assert obrigacao.nome == "Obrigações Teste"
    assert obrigacao.periodicidade == "mensal"
    assert obrigacao.empresa_id == empresa.id

# Função de teste para buscar todas as obrigacoes acessorias
def test_get_obrigacao_acessorias(setup_db):
    db, empresa = setup_db

    obrigacao_data = ObrigacaoAcessoriaCreate(
        nome="Obrigações Teste",
        periodicidade="mensal",
        empresa_id=empresa.id
    )
    create_obrigacao_acessoria(db, obrigacao_data)

    obrigacoes = get_obrigacoes_acessorias(db)
    assert len(obrigacoes) > 0
    assert obrigacoes[0].nome == "Obrigações Teste"

# Função de teste para buscar uma obrigacao acessoria por ID
def test_get_obrigacao_acessoria(setup_db):
    db, empresa = setup_db

    obrigacao_data = ObrigacaoAcessoriaCreate(
        nome="Obrigações Teste",
        periodicidade="mensal",
        empresa_id=empresa.id
    )
    obrigacao = create_obrigacao_acessoria(db, obrigacao_data)

    fetched_obrigacao = get_obrigacao_acessoria(db, obrigacao.id)

    assert fetched_obrigacao is not None
    assert fetched_obrigacao.id == obrigacao.id
    assert fetched_obrigacao.nome == "Obrigações Teste"
    assert fetched_obrigacao.periodicidade == "mensal"
    assert fetched_obrigacao.empresa_id == empresa.id

    # Função de teste para atualizar uma obrigacao acessoria
def test_update_obrigacao_acessoria(setup_db):
    db, empresa = setup_db

    # Criação de uma obrigação acessória inicial
    obrigacao_data = ObrigacaoAcessoriaCreate(
        nome="Obrigações Teste",
        periodicidade="mensal",
        empresa_id=empresa.id
    )
    obrigacao = create_obrigacao_acessoria(db, obrigacao_data)

    # Dados de atualização para a obrigação
    update_data = ObrigacaoAcessoriaCreate(
        nome="Obrigações Atualizadas",
        periodicidade="trimestral",
        empresa_id=empresa.id
    )

    # Atualizando a obrigação
    updated_obrigacao = update_obrigacao_acessoria(db, obrigacao.id, update_data)

    # Verificando se a atualização foi bem-sucedida
    assert updated_obrigacao is not None
    assert updated_obrigacao.id == obrigacao.id
    assert updated_obrigacao.nome == "Obrigações Atualizadas"
    assert updated_obrigacao.periodicidade == "trimestral"
    assert updated_obrigacao.empresa_id == empresa.id

# Função de teste para deletar uma obrigacao acessoria
def test_delete_obrigacao_acessoria(setup_db):
    db, empresa = setup_db

    # Criação de uma obrigação acessória inicial
    obrigacao_data = ObrigacaoAcessoriaCreate(
        nome="Obrigações Teste",
        periodicidade="mensal",
        empresa_id=empresa.id
    )
    obrigacao = create_obrigacao_acessoria(db, obrigacao_data)

    # Deletando a obrigação
    result = delete_obrigacao_acessoria(db, obrigacao.id)

    # Verificando se a obrigação foi deletada
    assert result is True

    # Verificando se a obrigação não está mais presente no banco de dados
    deleted_obrigacao = get_obrigacao_acessoria(db, obrigacao.id)
    assert deleted_obrigacao is None

