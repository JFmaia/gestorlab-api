## Rodando o Projeto:

#### Passo 1: Apos clonar o repositorio busque todas as branchs do repositorio que foi clonado e depois entre na branch ***developer***
> ``` git fetch ```
> ``` git checkout developer ```

#### Passo 2: Agora estando na branch ***developer*** crie seu ambiente de desenvolvimento python com virtualenv ou venv e entre nele
> ``` python3 -m venv "NOME_DO_AMBIENTE" ```>
> ``` source NOME_DO_AMBIENTE/bin/activate ```

#### Passo 3: Depois de está já no seu ambiente virtual instale no seu ambiente as dependecias do projeto.
> ```pip install -r requirements.txt```

#### Passo 4: Faça uma copia do arquivo ***.env.example***, renomei a copia para ***.env*** e por fim preencha os campos vazios que exitem em ***.env***, exemplo: ***POSTGRES_USER='useradmin'***.

#### Passo 5: Na pasta do ***alembic*** crie uma pasta chamada ***versions***.

#### Passo 6: Depois execute no terminal esse comando ``` docker compose up ``` se o seu docker não tem permissão sudo utilize ``` sudo docker compose up ``` isso fará uma imagem do banco de dados do Postgreys.
> ``` docker compose up ```
ou
> ``` sudo docker compose up ```

### Testes:

> Para rodar os testes utilize o comando ``` pytest -v ```, e todos os testes iram rodar.
