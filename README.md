# Projeto Django chamado Ado.te
Projeto desenvolvido em Django na versão 4.1.5
# Passo a passo para rodar o projeto

A primeiro coisa a fazer é clonar o repositorio
```sh
$ git clone https://github.com/JJtankevans/Ado.te.git
$ cd nome-da-pasta-em-que-voce-clonou
```
Em seguida cria o ambiente virtual e entre nele da seguinte maneira
```sh
$ virtualenv --no-site-packages venv
$ venv/bin/activate
```
Com o ambiente virtual ativo instale as dependências
```sh
(venv)$ pip install -r requirements.txt
```

Assim que o pip tiver terminado o download das dependências
```sh
(env)$ cd project
(env)$ python manage.py runserver
```

Caso aconteça algum erro ao tentar rodar o comando acim tente fazer as migrações primeiro rodando o comando
```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

Então vá para a o endereço ```sh http://127.0.0.1:8000/auth/cadastro/```