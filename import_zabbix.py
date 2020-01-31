#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
import csv
import sys
import json

# Variaveis
server =  sys.argv[1] #ip-do-zabbix
username = sys.argv[2] #usuario
password = sys.argv[3] #senha
arquivo = sys.argv[4]

# Loga no Zabbix Server
zapi = ZabbixAPI(server = server, path="")
zapi.login(username, password)

# Le o arquivo CSV
# Formato do CSV:
# Hostgroup;Template;Hostname;Visible name;DNS;IP;Agent type;Connect to;Proxy;Inventory;Macros
f = csv.reader(open(arquivo), delimiter=';') #lendo-a-lista de host e separando pelo delimatador ';'



for [hostgroup,template,hostname,alias,dns,ip,agent,connectto,proxy,inventory,macros] in f:
    
    print "+ Cadastrando o host " +  hostname
    #print hostgroup,template,hostname,alias,dns,ip,agent,connectto,proxy,inventory,macros
    ignora_host = False
    datajson = {}
    datajson['templates'] = []
    datajson['groups'] = []
    datajson['host'] = hostname
    datajson['name'] = alias
    datajson['interfaces'] = []
    templatejson = ""
    hostgroupjson = ""
    macrosjson = ""

    hostid = zapi.host.get({"output": "shorten","filter":{ "host": hostname }}) 

    if not hostid:
        
        for templateid in template.split(','):
            #print templateid
            # Verificando se existe o template informado
            templateid_tmp = zapi.template.get({"output": "shorten", "filter": { "host": templateid }})
            if not templateid_tmp:
                print(" - [ERRO] Template " + templateid + "nao existe! Ignorando criacao do host!")
                ignora_host = True
            else:
                templateid_nr = str( zapi.template.get({"output": "shorten", "filter": { "host": templateid }})[0]['templateid'] ) 

                datajson['templates'].append({'templateid':templateid_nr}) 

        if not ignora_host:

            for hostgroupid in hostgroup.split(','):
                #print hostgroupid
                
                if not ignora_host:
                    # Se hostgroup vazio, cria um novo
                    hostgroupid_tmp = zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroupid }})   
                    if not hostgroupid_tmp:
                        print(" - Host group nao existe, criando o hostgroup " + hostgroupid)
                        zapi.hostgroup.create({"name": hostgroupid })
                        # Validando se o hostgroup foi criado
                        hostgroupid_tmp = zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroupid }})

                    if not hostgroupid_tmp:
                        print(" - [ERRO] Hostgroup " + hostgroupid + " nao criado! Ignorando criacao do host!")
                        ignora_host = True
                    else:
                        hostgroupid_nr = str( zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroupid }})[0]['groupid'] )

                        datajson['groups'].append({'groupid':hostgroupid_nr})

            if not ignora_host:        
                if macros:
                    datajson['macros'] = []
                    for macrosid in macros.split(','):
                        macrosid_nr, macrosid_value = macrosid.split('=')
                        
                        macrosid_nr = '{$' + macrosid_nr + '}'
                        #print macrosid_nr, macrosid_value
                        datajson['macros'].append({'macro': macrosid_nr, 'value': macrosid_value})
            
            inventory = str(inventory)
            if inventory == "automatic" :
                inventoryid = 1
            elif inventory == "manual":
                inventoryid = 0
            else:
                inventoryid = -1

            #datajson['inventory'] = inventoryid

            if agent == "agent":
                agentid = 1
                portid = "10050"
            elif agent == "SNMP":
                agentid = 2
                portid = "161"
            elif agent == "IPMI":
                agentid = 3
            elif agent == "JMX":
                agentid = 4
            else:
                agentid = 2

            if connectto == "DNS":
                useip = 0
            else:
                useip = 1

            datajson['interfaces'].append({'type':agentid , 'main':'1', 'useip':useip, 'ip':ip, 'dns':dns,'port':portid})

            #print json.dumps(datajson) 

            #print(" - Criando host")
            zapi.host.create(datajson)
            #print("  -- Verificando se foi criado")
            hostid = str(zapi.host.get({"output": "shorten","filter":{ "host": hostname }})[0]['hostid'] )

            if hostid:
                print(" - [OK]: Host criado com sucesso")
            else:
                print(" - [ERRO]: Host nao criado")

    else:
        print(" - [ERRO]: Host ja existe! Ignorando a criacao deste host!")
