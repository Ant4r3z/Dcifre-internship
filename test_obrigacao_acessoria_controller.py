import pytest
from fastapi.testclient import TestClient
from main import app
import schemas

# Usando o TestClient do FastAPI para testar os endpoints
client = TestClient(app)

@pytest.fixture
def mock_service(mocker):
    # Mockando as funções da camada de service
    mock_create_obrigacao = mocker.patch('obrigacao_acessoria_service.create_obrigacao_acessoria')
    mock_get_obrigacoes = mocker.patch('obrigacao_acessoria_service.get_obrigacoes_acessorias')
    mock_get_obrigacao = mocker.patch('obrigacao_acessoria_service.get_obrigacao_acessoria')
    mock_update_obrigacao = mocker.patch('obrigacao_acessoria_service.update_obrigacao_acessoria')
    mock_delete_obrigacao = mocker.patch('obrigacao_acessoria_service.delete_obrigacao_acessoria')

    return {
        'create_obrigacao': mock_create_obrigacao,
        'get_obrigacoes': mock_get_obrigacoes,
        'get_obrigacao': mock_get_obrigacao,
        'update_obrigacao': mock_update_obrigacao,
        'delete_obrigacao': mock_delete_obrigacao,
    }

# Teste para o POST /obrigacoes/
def test_create_obrigacao_acessoria(mock_service):
    obrigacao_data = schemas.ObrigacaoAcessoriaCreate(
        nome="Obrigação Teste", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1
    )
    mock_service['create_obrigacao'].return_value = schemas.ObrigacaoAcessoria(
        id=1, nome="Obrigação Teste", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1
    )
    
    response = client.post("/obrigacoes/", json=obrigacao_data.model_dump())
    
    assert response.status_code == 201
    assert response.json()['nome'] == "Obrigação Teste"
    assert response.json()['empresa_id'] == 1

# Teste para o GET /obrigacoes/
def test_get_obrigacoes_acessorias(mock_service):
    mock_service['get_obrigacoes'].return_value = [
        schemas.ObrigacaoAcessoria(id=1, nome="Obrigação 1", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1),
        schemas.ObrigacaoAcessoria(id=2, nome="Obrigação 2", periodicidade=schemas.PeriodicidadeEnum.ANUAL, empresa_id=2)
    ]
    
    response = client.get("/obrigacoes/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['nome'] == "Obrigação 1"
    assert response.json()[1]['nome'] == "Obrigação 2"

# Teste para o GET /obrigacoes/{obrigacao_id}
def test_get_obrigacao_acessoria(mock_service):
    obrigacao_id = 1
    mock_service['get_obrigacao'].return_value = schemas.ObrigacaoAcessoria(
        id=obrigacao_id, nome="Obrigação Teste", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1
    )
    
    response = client.get(f"/obrigacoes/{obrigacao_id}")
    
    assert response.status_code == 200
    assert response.json()['nome'] == "Obrigação Teste"
    assert response.json()['empresa_id'] == 1

# Teste para o PUT /obrigacoes/{obrigacao_id}
def test_update_obrigacao_acessoria(mock_service):
    obrigacao_id = 1
    obrigacao_update_data = schemas.ObrigacaoAcessoriaBase(nome="Obrigação Atualizada", periodicidade=schemas.PeriodicidadeEnum.TRIMESTRAL)
    
    mock_service['update_obrigacao'].return_value = schemas.ObrigacaoAcessoria(
        id=obrigacao_id, nome="Obrigação Atualizada", periodicidade=schemas.PeriodicidadeEnum.TRIMESTRAL, empresa_id=1
    )
    
    response = client.put(f"/obrigacoes/{obrigacao_id}", json=obrigacao_update_data.model_dump())
    
    assert response.status_code == 200
    assert response.json()['nome'] == "Obrigação Atualizada"
    assert response.json()['periodicidade'] == schemas.PeriodicidadeEnum.TRIMESTRAL

# Teste para o DELETE /obrigacoes/{obrigacao_id}
def test_delete_obrigacao_acessoria(mock_service):
    obrigacao_id = 1
    mock_service['delete_obrigacao'].return_value = {"message": "Obrigação acessória excluída com sucesso"}
    
    response = client.delete(f"/obrigacoes/{obrigacao_id}")
    
    assert response.status_code == 204
