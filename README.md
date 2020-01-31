zabbix-import
=============

Script desenvolvido em Python que permite importar hosts no Zabbix através de um arquivo de entrada (.csv).

### Pré-requisito

Python
Zabbix API in Python


### Instalação

1. Faça o clone deste projeto 

`$ git clone https://github.com/sbaron81/zabbix-import.git`

2. Instale o Zabbix API: 

`$ pip install zabbix-api`

3. Entre na pasta do projeto

`$ cd zabbix-import`

4. Crie o arquivo csv com as informações a serem importados, conforme o cabeçalho:

`Hostgroup;Template;Hostname;Visible name;DNS;IP;Agent type;Connect to;Proxy;Inventory;Macros`

Obs: Não inclua o cabeçalho no arquivo, o arquivo csv deve ter somente os dados a serem importados.

Exemplo:

`$ cat arquivo_exemplo.csv  
Producao;Template - Linux;servidor1;Servidor producao 01;servidor1.dominio.com;10.1.1.1;agent;ip;none;automatic;MY_MACRO=ABC,MY_SECOND_MACRO=EFG  
Producao,Switches;Template - Switches,Template - Switch HPE;SW-ACESSO-001;Switch de Acesso 001;;10.1.10.5;SNMP;ip;none;automatic;SNMPCOMMUNITY=public`

5. Rode o script 

`$ python import_zabbix.py "http://servidor/zabbix" "usuario" "minhasenha" arquivo_exemplo.csv`

