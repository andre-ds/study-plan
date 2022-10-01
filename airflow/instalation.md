
# Instalação do Apache Airflow

## Definindo a Variável de Ambiente

O primeiro passo para a instalação do airflow é a definição da variável de ambiente que pode ser feita de forma termporária ou permanente.

* Temporária:

export AIRFLOW_HOME=$(pwd)/airflow

* Permanente: 

Na seção Linux - environmental_variables.md eu demonstro como criar uma variável de ambiente permanete.


## Instalação via pip

Para fazer a instalção via pip seguindo a recomendação da apache airflow é importante definir alguns constraint, para isso e também com o objetivo de obter a versão mais atual eu recomendo copiar o comando de instalação diretamente no site do airflow, neste momento o link é o seguinte:

* Link: **https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html**

* Para fazer a instalação, basta digitar o seguinte comando no terminal na pasta onde você deseja instalar:

*pip install "apache-airflow[celery]==2.3.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.3.3/constraints-3.7.txt"*


## Inicialização do Banco de Dados

Após a instalação ser completada é necessário inicializar o banco de dados. Neste exemplo por não ser um ambiente produtivo vamos utilizar o banco de dados que default do airflow sqlite.

* Basta digitar:
*airflow db init*


## Criação do Usuário

* Para criar o usuário de acesso, digite o seguinte comando:

*airflow users create \\
    --username admin \\
    --firstname Plinio \\
    --lastname Silva \\
    --role Admin \\
    --email pliniosilva@gmail.com*

Em seguida será necessário digitar o password e confirmá-lo.


## Inicialização do Airflow

Para iniciar o airflow é necessário iniciar o Webserver, serviço responsável pela interface da ferramenta e o Scheduler, responsável pelo agendamento das tarefas de execução. Respectivamente, para iniciá-los, digite:

* Webserver:

airflow webserver -p 8080

* Scheduler:

airflow scheduler

Obs: Digitando os comandos desta forma, você ficará conectado aos terminais, portanto, será necessário abrir um terminal para cada serviço. Para não ficar conectado 

## Acessando a Interface no Navegador

Com os dois serviços ativados basta entrar no seguinte link no seu navegador: http://localhost:8080
