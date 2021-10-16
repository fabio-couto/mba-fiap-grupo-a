# MBA Fiap - Grupo A - Case da Usina de Cana de Açucar

## Objetivo

Disponibilizar um ambiente virtualizado de Big Data para avaliação e testes da proposta de solução do case da Usina de Cana de Açucar do Grupo A

## Diretórios

* ./docker-hadoop: Possui todas os arquivos para build das imagens e start dos contêineres
* ./datalake: Código fonte da solução (Programas Python e Estruturas de dados)

## Pré requisitos para execução

- Docker e Docker Compose (Inclusos no [Docker Desktop](https://www.docker.com/products/docker-desktop))

## Como subir o ambiente

Primeiro, efetue o build da imagem base com o comando abaixo (*Este build poderá levar alguns minutos):

`docker build -t hadoop-base:0.1.0 .\docker-hadoop\00_hadoop-base\`

Depois do build da image base, para subir os contêineres, utilize o comando abaixo:

`docker-compose -f .\docker-hadoop\docker-compose.yml up -d`

Os serviços serão iniciados nos endereços abaixo

- Namenode: http://localhost:50070/
- Datanode 1: http://localhost:50075/
- Datanode 2: http://localhost:50076/
- Datanode 3: http://localhost:50077/
- Resource Manager: http://localhost:8088/
- History Server: http://localhost:8188/
- Hue: http://localhost:8888/
- HiveServer2 UI: http://localhost:10002/ (*Este serviço leva alguns segundos para iniciar*)
- Kafdrop: http://localhost:19000
- InfluxDb: http://127.0.0.1:8086
- Grafana: http://127.0.0.1:13000

## Como encerrar o ambiente

Utilize o comando abaixo:

`docker-compose -f .\docker-hadoop\docker-compose.yml down`