import pytest
from fastapi.testclient import TestClient
from main import app
import schemas

# Usando o TestClient do FastAPI para testar os endpoints
client = TestClient(app)

@pytest.fixture
def mock_service(mocker):
    # Mockando as funções da camada de service
    mock_create_empresa = mocker.patch('empresa_service.create_empresa')
    mock_get_empresas = mocker.patch('empresa_service.get_empresas')
    mock_get_empresa = mocker.patch('empresa_service.get_empresa')
    mock_update_empresa = mocker.patch('empresa_service.update_empresa')
    mock_delete_empresa = mocker.patch('empresa_service.delete_empresa')

    return {
        'create_empresa': mock_create_empresa,
        'get_empresas': mock_get_empresas,
        'get_empresa': mock_get_empresa,
        'update_empresa': mock_update_empresa,
        'delete_empresa': mock_delete_empresa,
    }


# Teste para o POST /empresas/
def test_create_empresa(mock_service):
    # Dados da empresa a ser criada
    empresa_data = schemas.EmpresaCreate(
        nome="Empresa Teste", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="123456789"
    )
    
    # Mockando o retorno da função de service
    mock_service['create_empresa'].return_value = schemas.Empresa(
        id=1, nome="Empresa Teste", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="123456789", obrigacoes=[]
    )
    
    response = client.post("/empresas/", json=empresa_data.model_dump())

    assert response.status_code == 201
    assert response.json()['nome'] == "Empresa Teste"
    assert response.json()['cnpj'] == "12345678000195"
    assert response.json()['telefone'] == "123456789"


# Teste para o GET /empresas/
def test_get_empresas(mock_service):
    # Mockando o retorno da função de service
    mock_service['get_empresas'].return_value = [
        schemas.Empresa(id=1, nome="Empresa Teste", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="123456789", obrigacoes=[]),
        schemas.Empresa(id=2, nome="Empresa Teste 2", cnpj="98765432000199", endereco="Rua Teste 2, 456", email="teste2@empresa.com", telefone="987654321", obrigacoes=[])
    ]
    
    response = client.get("/empresas/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['nome'] == "Empresa Teste"
    assert response.json()[1]['nome'] == "Empresa Teste 2"


# Teste para o GET /empresas/{empresa_id}
def test_get_empresa(mock_service):
    empresa_id = 1
    mock_service['get_empresa'].return_value = schemas.Empresa(
        id=empresa_id, nome="Empresa Teste", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="123456789", obrigacoes=[]
    )
    
    response = client.get(f"/empresas/{empresa_id}")

    assert response.status_code == 200
    assert response.json()['nome'] == "Empresa Teste"
    assert response.json()['cnpj'] == "12345678000195"


# Teste para o PUT /empresas/{empresa_id}
def test_update_empresa(mock_service):
    empresa_id = 1
    empresa_update_data = schemas.EmpresaUpdate(nome="Empresa Teste Atualizada", telefone="987654321")

    # Mockando o retorno da função de service
    mock_service['update_empresa'].return_value = schemas.Empresa(
        id=empresa_id, nome="Empresa Teste Atualizada", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="987654321", obrigacoes=[]
    )
    
    response = client.put(f"/empresas/{empresa_id}", json=empresa_update_data.model_dump())

    assert response.status_code == 200
    assert response.json()['nome'] == "Empresa Teste Atualizada"
    assert response.json()['telefone'] == "987654321"


# Teste para o DELETE /empresas/{empresa_id}
def test_delete_empresa(mock_service):
    empresa_id = 1
    # Mockando a função de delete
    mock_service['delete_empresa'].return_value = {"message": "Empresa excluída com sucesso"}

    response = client.delete(f"/empresas/{empresa_id}")

    assert response.status_code == 204
