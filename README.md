## Rodando o Projeto:

> 1. Ao clonar o projeto crie seu ambiente de desenvolvimento python com virtualenv ou venv e entre nele.

> 2. Depois de está já no seu ambiente virtual rode ``` pip install -r requirements.txt ```, para instalar em seu ambiente as dependecias do projeto.

> 3. Depois da instalação faça uma copia do arquivo ** .env.example ** e renomei essa compia para **.env**, por fim na **.env** preencha as variaveis que estão vazias.
- OBS: Lembre-se de preenche-las com dados diferentes para que as variaves de test não sejam iguais.
  
> 4. Logo depois de preenche-las rode o comando no terminal ``` docker compose up ```, para que ambos os bancos sejam criados.

> 5. Apois crie os modelos no banco utilizando o comando no terminal ``` python3 create_tables.py ```.

> 6. Por fim rode o projeto com o comando ``` python3 main.py ```

### Testes:

> Para rodar os testes utilize o comando ``` pytest ```, e todos os testes iram rodar.
