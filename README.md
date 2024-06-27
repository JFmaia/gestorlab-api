## Rodando o Projeto:

#### Passo 1: Apos clonar o repositorio busque todas as branchs do repositorio que foi clonado e depois entre na branch ***developer***
- ``` git fetch ```
- ``` git checkout developer ```

#### Passo 2: Agora estando na branch ***developer*** crie seu ambiente de desenvolvimento python com virtualenv ou venv e entre nele
- ``` python3 -m venv "NOME_DO_AMBIENTE" ```
- ``` source NOME_DO_AMBIENTE/bin/activate ```

#### Passo 3: Depois de está já no seu ambiente virtual rode ```pip install -r requirements.txt```, para instalar no seu ambiente as dependecias do projeto.

#### Passo 4: Faça uma copia do arquivo ***.env.example***, renomei a copia para ***.env*** e por fim preencha os campos vazios que exitem em ***.env***, exemplo: ***POSTGRES_USER='useradmin'***

#### Passo 5: Depois execute no terminal esse comando ``` docker compose up ``` se o seu docker não tem permissão sudo utilize ``` sudo docker compose up ``` isso fará uma imagem do banco de dados do Postgreys.

#### Passo 6: Crie uma pasta chamada "versions" dentro da pasta ***alembic***, depois disso vai no terminal e digite ``` alembic revision --autogenerate -m "Migração inicial!" ```, assim será feito a a criação de migration e assim você poderá executar no terminal ``` alembic upgrade head ``` o alembic pegará a ultima migration e adicionara todas as mudanças no banco de dados que no ultmi passo você ativou.

#### Passo 7: Execute no terminal o comando ``` python create_utils.py ``` isso irá popular algumas tabelas do banco de dados padrões e necessarios.

#### Passo 8: Para testar a api rodando execute o comando ``` python main.py ```, assim aplicação se inicializa, para acessar use ```http://localhost:8000/docs```, onde será visto todos os endpoints.

### Testes:

> Para rodar os testes utilize o comando ``` pytest -v ```, e todos os testes iram rodar.
