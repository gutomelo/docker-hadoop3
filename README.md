# :elephant: |Rodando o Hadoop 3.3.0 no Docker| :ship:

<p align="justify">
Este guia tem como princípio auxiliar na execução do Hadoop Map Reduce via Docker. Realizando testes de um job map reduce com Java e uma job em Python através do Hadoop Streaming. Os códigos das jobs de exemplo foram retirados do livro ["The Hadoop Fundamentals for Data Scientists"](https://github.com/bbengfort/hadoop-fundamentals).

Lembrando que nesse guia não mostrarei como foi feito a instalação do Hadoop no Docker.A imagem já está pronta, basta seguir as instruções para fazer o teste.
</p>

Os passos a seguir foram feitos numa máquina Linux com a distribuição do Ubuntu.

#### Antes de tudo você precisa ter o docker instalado, para isso execute o comando a seguir caso não tenha:
> sudo apt-get install docker.io

#### Liste os container em execução para saber se o docker está em funcionamento.
> sudo docker ps -a

#### Faça o Download da imagem Docker.
> sudo docker pull gutomelo/hadoop3

#### Após o Download da imagem, criar o container Hadoop.
> sudo docker run -it --name Hadoop -d -p 9870:9870 -p 8088:8088 gutomelo/hadoop3:latest

##### Aguarde alguns segundos, para que todos os serviços do Hadoop sejam executados.

#### Visualizando o portal do Name Node do Hadoop.
> http://localhost:9870

#### Visualizando o portal do YARN.
> http://localhost:8088

-----

## Realizando testes com uma job MapReduce em JAVA

A imagem já vem com os arquivos de testes, que inclusive já se encontra nesse repositório.

#### Para isso primeiro acesse o terminal do container
> sudo docker exec -it Hadoop sh

#### Entre no modo super usuario, pois nesse caso o hadoop só pode ser executado com ele.
> sudo su

#### Verificando se os seis serviços hadoop está em execução
> jps

#### Acessando a pasta com os arquivos job em Java
> cd /home/docker-hadoop3/WordCount

##### Agora nesse momento iremos compilar os arquivos Java, lembrando que devemos que compilar os três arquivos, porque um é dependente dos outros.

#### Compilando os arquivos Java na pasta

> hadoop com.sun.tools.javac.Main WordCount.java WordMapper.java SumReducer.java

##### Se você der o comandos 'ls', verá que foi criado os três arquivos .class "WordCount.class WordMapper.class SumReducer.class"

#### Agora vamos gerar o arquivo .Jar que será executado na instrução do Job MapReduce
> jar cf wc.jar WordCount.class WordMapper.class SumReducer.class

##### OBS: Os arquivos de inputs "shakespeare.txt" e "names.txt" já foram inseridos no hdfs através dos comandos "hadoop fs -put origemlocal destinohdfs". Ex: "hadoop fs -put /home/docker-hadoop3/WordCount/names.txt /"

#### Agora sim vamos fazer a execução do Job MapReducer Java no Hadoop
> hadoop jar wc.jar WordCount /shakespeare.txt /wordcounts

#### Verificando a pasta de resultado do Job "wordcounts" no HDFS
> hadoop fs -ls /wordcounts

#### Verificando a contagem de palavras do resultado da Job "wordcounts"
> hadoop fs -cat /wordcounts/part-r-00000

#### Podemos fazer novamente uma nova Job com o arquivo de input "names.txt"
> hadoop jar wc.jar WordCount /names.txt /namescounts

#### Verificando a pasta de resultado do Job "wordcounts" no HDFS
> hadoop fs -ls /namescounts

#### Verificando a contagem de palavras do resultado da Job "wordcounts"
> hadoop fs -cat /namescounts/part-r-00000

-----

### Realizando testes com uma job MapReduce em Python com o Hadoop Streaming

#### Acessando a pasta com os arquivos job em Python
> cd /home/docker-hadoop3/StreamingWordCount

#### Agora executamos a Job MapReduce "wordcounts" do cógido Python
> mapred streaming -input /shakespeare.txt -output /shakespeare_python -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py

#### Verificando a pasta de resultado do Job "shakespeare_python" no HDFS
> hadoop fs -ls /shakespeare_python

#### Verificando a contagem de palavras do resultado da Job "shakespeare_python"
> hadoop fs -cat /shakespeare_python/part-00000

#### Agora executamos a Job MapReduce "names" do cógido Python
> mapred streaming -input /names.txt -output /names_python -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py

#### Verificando a pasta de resultado do Job "names_python" no HDFS
> hadoop fs -ls /names_python

#### Verificando a contagem de palavras do resultado da Job "names_python"
> hadoop fs -cat /names_python/part-00000