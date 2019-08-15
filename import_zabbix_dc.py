#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
import csv
import sys


server =  sys.argv[1] #ip-do-zabbix
username = sys.argv[2] #usuario
password = sys.argv[3] #senha
arquivo = sys.argv[4]

zapi = ZabbixAPI(server = server, path="")
zapi.login(username, password)

# Hostgroup;Template;Hostname;Visible name;DNS;IP;Agent type;Connect to;Proxy;Inventory;Macros
f = csv.reader(open(arquivo), delimiter=';') #lendo-a-lista de host e separando pelo delimatador ';'

for [hostgroup,template,hostname,alias,dns,ip,agent,connectto,proxy,inventory,macros] in f:

    hostgroupid = zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroup }})   
    # Se hostgroup vazio, cria um novo
    if not hostgroupid:
        #zapi.hostgroup.create({"name": hostgroup })
        print("Host group nao existe!!!")
    hostgroupid = str( zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroup }})[0]['groupid'] )

    templateid = str( zapi.template.get({"output": "shorten", "filter": { "host": template }})[0]['templateid'] ) 
    teste = "automatic"
    if inventory is teste :
        inventoryid = 1
        print(inventory,inventoryid)
    elif inventory is 'manual':
        inventoryid = 0
        print(inventory,inventoryid)
    else:
        inventoryid = -1
        print(inventory,inventoryid)
    print(inventory,inventoryid)

    #if inventory is not "" or inventory is not "none" :
    #   proxyid = str( zapi.proxy.get( {"output": "shorten","filter":{ "host": proxy } })[0]['proxyid'] )
    print("--")
    hostid = zapi.host.get({"output": "shorten","filter":{ "host": hostname }}) 

    print(hostgroup,hostgroupid,template,templateid,hostname,alias,dns,ip,agent,connectto,proxy,inventory,inventoryid,macros)

    if hostid:
         print("Host ja existe")
    else: 
         print("Criando host")
         zapi.host.create({
                "host": hostname,
                "name": alias,
                "interfaces": [{
                    "type": "1",
                    "main": "1",
                    "useip": "0",
                    "ip": ip,
                    "dns": dns,
                    "port": 10050 }],
                "groups": [{ "groupid": hostgroupid }], #id do host grupo
                "templates": [{ "templateid": templateid }] #id do template
                #"inventory_mode" : inventoryid
         })
    print("Verificando se foi criado")
    hostid = str(zapi.host.get({"output": "shorten","filter":{ "host": hostname }})[0]['hostid'] )

    if hostid:
        print("Host criado com sucesso")
    else:
        print("Host nao criado")
    
         #if ip_internet:
         #   zapi.usermacro.create({
         #       "hostid": hostid,
         #       "macro": "{$IP_INTERNET}",
         #       "value": ip_internet
         #  }) 

