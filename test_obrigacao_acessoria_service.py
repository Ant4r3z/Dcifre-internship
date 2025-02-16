import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from empresa_service import create_empresa
from obrigacao_acessoria_service import create_obrigacao_acessoria, get_obrigacao_acessoria, get_obrigacoes_acessorias, update_obrigacao_acessoria, delete_obrigacao_acessoria
import schemas


# Teste para a criação de obrigacao acessoria
def test_create_obrigacao_acessoria(mocker):
    mock_db = mocker.Mock(spec=Session)
    obrigacao_data = schemas.ObrigacaoAcessoriaCreate(
        nome="Obrigação Acessoria Teste",
        periodicidade=schemas.PeriodicidadeEnum.MENSAL,
        empresa_id=1
    )

    # Mockando a função create_obrigacao_acessoria do repositório
    mock_create_obrigacao = mocker.patch('obrigacao_acessoria_repository.create_obrigacao_acessoria')
    mock_create_obrigacao.return_value = schemas.ObrigacaoAcessoria(
        id=1, nome="Obrigação Acessoria Teste", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1
    )

    # Chamando a função de service
    obrigacao_criada = create_obrigacao_acessoria(mock_db, obrigacao_data)

    # Verificando os resultados
    assert obrigacao_criada.nome == "Obrigação Acessoria Teste"
    assert obrigacao_criada.periodicidade == schemas.PeriodicidadeEnum.MENSAL
    assert obrigacao_criada.empresa_id == 1


# Teste para a função que recupera todas as obrigações acessórias
def test_get_obrigacoes_acessorias(mocker):
    mock_db = mocker.Mock(spec=Session)

    # Mockando a função get_obrigacoes_acessorias do repositório
    mock_get_obrigacoes = mocker.patch('obrigacao_acessoria_repository.get_obrigacoes_acessorias')
    mock_get_obrigacoes.return_value = [
        schemas.ObrigacaoAcessoria(id=1, nome="Obrigação Acessoria Teste", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1)
    ]

    # Chamando a função de service
    obrigacoes = get_obrigacoes_acessorias(mock_db)

    # Verificando se a função retornou corretamente
    assert len(obrigacoes) > 0
    assert obrigacoes[0].nome == "Obrigação Acessoria Teste"


# Teste para a função que recupera uma obrigação acessoria por ID
def test_get_obrigacao_acessoria(mocker):
    mock_db = mocker.Mock(spec=Session)
    obrigacao_id = 1

    # Mockando a função get_obrigacao_acessoria do repositório
    mock_get_obrigacao = mocker.patch('obrigacao_acessoria_repository.get_obrigacao_acessoria')
    mock_get_obrigacao.return_value = schemas.ObrigacaoAcessoria(
        id=1, nome="Obrigação Acessoria Teste", periodicidade=schemas.PeriodicidadeEnum.MENSAL, empresa_id=1
    )

    # Chamando a função de service
    obrigacao = get_obrigacao_acessoria(mock_db, obrigacao_id)

    # Verificando se a obrigação acessória foi encontrada corretamente
    assert obrigacao is not None
    assert obrigacao.nome == "Obrigação Acessoria Teste"


# Teste para a função que atualiza uma obrigação acessoria
def test_update_obrigacao_acessoria(mocker):
    mock_db = mocker.Mock(spec=Session)
    obrigacao_id = 1
    obrigacao_data = schemas.ObrigacaoAcessoriaUpdate(nome="Obrigação Acessoria Atualizada", periodicidade=schemas.PeriodicidadeEnum.TRIMESTRAL)

    # Mockando a função update_obrigacao_acessoria do repositório
    mock_update_obrigacao = mocker.patch('obrigacao_acessoria_repository.update_obrigacao_acessoria')
    mock_update_obrigacao.return_value = schemas.ObrigacaoAcessoria(
        id=1, nome="Obrigação Acessoria Atualizada", periodicidade=schemas.PeriodicidadeEnum.TRIMESTRAL, empresa_id=1
    )

    # Chamando a função de service
    obrigacao_atualizada = update_obrigacao_acessoria(mock_db, obrigacao_id, obrigacao_data)

    # Verificando se a atualização ocorreu corretamente
    assert obrigacao_atualizada is not None
    assert obrigacao_atualizada.nome == "Obrigação Acessoria Atualizada"
    assert obrigacao_atualizada.periodicidade == schemas.PeriodicidadeEnum.TRIMESTRAL


# Teste para a função que deleta uma obrigação acessoria
def test_delete_obrigacao_acessoria(mocker):
    mock_db = mocker.Mock(spec=Session)
    obrigacao_id = 1

    # Mockando a função delete_obrigacao_acessoria do repositório
    mock_delete_obrigacao = mocker.patch('obrigacao_acessoria_repository.delete_obrigacao_acessoria')
    mock_delete_obrigacao.return_value = True  # Simulando sucesso na exclusão

    # Chamando a função de service
    result = delete_obrigacao_acessoria(mock_db, obrigacao_id)

    # Verificando se a obrigação acessória foi deletada corretamente
    assert result == {"message": "Obrigação acessória excluída com sucesso"}

    # Verificando o comportamento quando a obrigação acessória não for encontrada
    mock_delete_obrigacao.return_value = False
    with pytest.raises(HTTPException) as excinfo:
        delete_obrigacao_acessoria(mock_db, obrigacao_id)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Obrigação acessória não encontrada"
