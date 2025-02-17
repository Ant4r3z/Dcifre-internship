# Dcifre-internship
Este projeto consiste na implementação de uma API para o cadastramento de empresas e gerenciamento de obrigações acessórias que a empresa precisa declarar para o governo. 

A API foi desenvolvida utilizando:

- **FastAPI** para criação dos endpoints
- **Pydantic** para validação dos dados
- **SQLAlchemy** para interação com o banco de dados PostgreSQL
- **Pytest** para criação de testes unitários

# Configuração do Ambiente

## Clonar o Repositório
```
git clone https://github.com/Ant4r3z/Dcifre-internship
cd Dcifre-internship
```

## Criar um Ambiente Virtual
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

## Instalar Dependências
```
pip install -r requirements.txt
```

## Criar um arquivo .env
```
DB_PASSWORD=''
DB_DATABASE=''
DB_USERNAME=''
```

## Subir o Banco de Dados com Docker
```
docker-compose up -d
```

## Rodar a API
PS: As tabelas serão criadas assim que o app for iniciado
```
uvicorn main:app --reload
```


# **Requisitos do Projeto**  

## ✅ **1. Configuração do Ambiente**  
- O ambiente virtual foi criado para gerenciar as dependências do projeto.  
- O **Docker Compose** foi adicionado para facilitar a configuração e execução do banco de dados PostgreSQL.  

## ✅ **2. Modelagem de Dados**  
- Modelagem realizada com **SQLAlchemy** e **Pydantic**, garantindo a integridade dos dados.  
- Definição das entidades **Empresa** e **Obrigação Acessória**, com relacionamento entre elas.  
- Utilização de **modelos SQLAlchemy** para persistência e **schemas Pydantic** para entrada e saída de dados.  

## ✅ **3. Implementação do CRUD**  
- CRUD implementado e organizado em **três camadas**:  
  - **Repositórios** (operações diretas no banco de dados)  
  - **Serviços** (regras de negócio e validações)  
  - **Controllers** (definição dos endpoints FastAPI)  
- Tratamento de erros aplicado para garantir respostas apropriadas.  
- Retorno correto de **códigos de status HTTP** em todas as operações.  

📌 Nota: A minha ideia inicial era separar as camadas em pastas (controllers, services, repositories e tests).
No entanto, como um dos requisitos era não criar subpastas, a estrutura ficou centralizada na raiz do projeto.

## ✅ **4. Banco de Dados e Configuração**  
- O projeto inclui um **arquivo `.env` de exemplo** no repositório para facilitar a configuração.  
- A conexão com o banco de dados é feita no arquivo `database.py`.  
- O banco de dados é levantado automaticamente via **Docker Compose**.  
- A criação das tabelas é feita automaticamente ao iniciar a aplicação, usando `models.Base.metadata.create_all(bind=engine)`, eliminando a necessidade de um script de migração separado.  

## ✅ **5. Testes e Documentação**  
- **Testes unitários** implementados utilizando **Pytest** e **Pytest-mock**.  
- Documentação automática da API disponível via **Swagger UI** (`/docs`).  


<br />
<p align="right"> <em> Made by 🐜4r3z </em> </p>