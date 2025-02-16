import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from empresa_service import create_empresa, get_empresas, get_empresa, update_empresa, delete_empresa
import schemas

# Teste para a criação de empresa
def test_create_empresa(mocker):
    mock_db = mocker.Mock(spec=Session)
    empresa_data = schemas.EmpresaCreate(
        nome="Empresa Teste",
        cnpj="12345678000195",
        endereco="Rua Teste, 123",
        email="teste@empresa.com",
        telefone="123456789"
    )
    
    # Mockando a função create_empresa do repository
    mock_create = mocker.patch('empresa_repository.create_empresa')
    mock_create.return_value = empresa_data  # Simulando a criação da empresa

    # Chamando a função de service
    empresa_criada = create_empresa(mock_db, empresa_data)

    # Verificando os resultados
    assert empresa_criada.nome == "Empresa Teste"
    assert empresa_criada.cnpj == "12345678000195"
    assert empresa_criada.endereco == "Rua Teste, 123"
    assert empresa_criada.email == "teste@empresa.com"
    assert empresa_criada.telefone == "123456789"

# Teste para a função que recupera todas as empresas
def test_get_empresas(mocker):
    mock_db = mocker.Mock(spec=Session)
    
    # Mockando a função get_empresas do repository
    mock_get_empresas = mocker.patch('empresa_repository.get_empresas')
    mock_get_empresas.return_value = [schemas.Empresa(id =1, nome="Empresa 1", cnpj="12345678000195", endereco="Rua 1", email="email@empresa.com", telefone="123456789", obrigacoes=[])]

    # Chamando a função de service
    empresas = get_empresas(mock_db)

    # Verificando se a função retornou corretamente
    assert len(empresas) > 0
    assert empresas[0].nome == "Empresa 1"

# Teste para a função que recupera uma empresa por ID
def test_get_empresa(mocker):
    mock_db = mocker.Mock(spec=Session)
    empresa_id = 1
    
    # Mockando a função get_empresa do repository
    mock_get_empresa = mocker.patch('empresa_repository.get_empresa')
    mock_get_empresa.return_value = schemas.Empresa(id=1, nome="Empresa Teste", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="123456789", obrigacoes=[])

    # Chamando a função de service
    empresa = get_empresa(mock_db, empresa_id)

    # Verificando se a empresa foi encontrada corretamente
    assert empresa is not None
    assert empresa.nome == "Empresa Teste"

# Teste para a função que atualiza uma empresa
def test_update_empresa(mocker):
    mock_db = mocker.Mock(spec=Session)
    empresa_id = 1
    empresa_data = schemas.EmpresaUpdate(nome="Empresa Teste", telefone="123456789")
    
    # Mockando a função update_empresa do repository
    mock_update_empresa = mocker.patch('empresa_repository.update_empresa')
    mock_update_empresa.return_value = schemas.Empresa(id=1, nome="Empresa Teste Atualizada", cnpj="12345678000195", endereco="Rua Teste, 123", email="teste@empresa.com", telefone="987654321", obrigacoes=[])

    # Chamando a função de service
    empresa_atualizada = update_empresa(mock_db, empresa_id, empresa_data)

    # Verificando se a atualização ocorreu corretamente
    assert empresa_atualizada is not None
    assert empresa_atualizada.nome == "Empresa Teste Atualizada"
    assert empresa_atualizada.telefone == "987654321"

# Teste para a função que deleta uma empresa
def test_delete_empresa(mocker):
    mock_db = mocker.Mock(spec=Session)
    empresa_id = 1
    
    # Mockando a função delete_empresa do repository
    mock_delete_empresa = mocker.patch('empresa_repository.delete_empresa')
    mock_delete_empresa.return_value = True  # Simulando sucesso na exclusão

    # Chamando a função de service
    result = delete_empresa(mock_db, empresa_id)

    # Verificando se a empresa foi deletada corretamente
    assert result == {"message": "Empresa excluída com sucesso"}
    
    # Verificando o comportamento quando a empresa não for encontrada
    mock_delete_empresa.return_value = False
    with pytest.raises(HTTPException) as excinfo:
        delete_empresa(mock_db, empresa_id)
    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == f"Erro ao excluir empresa com ID {empresa_id}"
