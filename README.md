## Rodando o Projeto:

#### Passo 1: Apos clonar o repositorio busque todas as branchs do repositorio que foi clonado e depois entre na branch ***develop***
- ``` git fetch ```
- ``` git checkout develop ```

#### Passo 2: Agora estando na branch ***develop*** crie seu ambiente de desenvolvimento python com virtualenv ou venv e entre nele
- ``` python3 -m venv "NOME_DO_AMBIENTE" ```
- ``` source NOME_DO_AMBIENTE/bin/activate ```

#### Passo 3: Depois de está já no seu ambiente virtual rode ```pip install -r requirements.txt```, para instalar no seu ambiente as dependecias do projeto.

#### Passo 4: Faça uma copia do arquivo ***.env.example***, renomei a copia para ***.env*** e por fim preencha os campos vazios que exitem em ***.env***, exemplo: *** POSTGRES_USER='useradmin' ***

#### Passo 5: Crie uma pasta chamada "versions" dentro da pasta ***alembic***, depois disso vai no terminal e digite ```docker compose up```, assim será feito a a criação de migration, implementada no banco e tbm a inicialização do projeto tbm já vai ser feita!

#### Passo 6: Para testar a api rodando use ```http://localhost:8000/docs```, onde será visto todos os endpoints.

### Testes:

> Para rodar os testes utilize o comando ``` pytest -v ```, e todos os testes iram rodar.
