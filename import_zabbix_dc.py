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

#Hostgroup;Template;hostname;Alias;IP;DNS
f = csv.reader(open(arquivo), delimiter=';') #lendo-a-lista de host e separando pelo delimatador ';'

for [hostgroup,template,hostname,alias,dns,ip] in f:

    hostgroupid = zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroup }})   
    # Se hostgroup vazio, cria um novo
    if not hostgroupid:
        #zapi.hostgroup.create({"name": hostgroup })
        print("Host group nao existe!!!")
    hostgroupid = str( zapi.hostgroup.get({"output": "shorten","filter":{ "name": hostgroup }})[0]['groupid'] )

    templateid = str( zapi.template.get({"output": "shorten", "filter": { "host": template }})[0]['templateid'] ) 

    inventoryid = 1
    #if inventory is "Automatic":
    #    inventoryid = 1
    #elif inventory is "Manual":
    #    inventoryid = 0
    #else:
    #    inventoryid = -1
    #proxyid = str( zapi.proxy.get( {"output": "shorten","filter":{ "host": proxy } })[0]['proxyid'] )

    hostid = zapi.host.get({"output": "shorten","filter":{ "host": hostname }}) 

    print(hostgroup,hostgroupid,hostid,template,templateid,hostname,alias,dns,ip,inventoryid)

    if hostid:
         print("Host ja existe")
    else: 
         print("Cria host")
         zapi.host.create({
                "host": hostname,
                "name": alias,
                "interfaces": [ {"type": "1",
                    "default": "1",
                    "useip": "0",
                    "ip": ip,
                    "dns": dns }],
                "groups": [{ "groupid": hostgroupid }], #id do host grupo
                "templates": [{ "templateid": templateid }] , #id do template
                "inventory_mode" : inventoryid
         })
         hostid = str( zapi.host.get({"output": "shorten","filter":{ "host": hostname }})[0]['hostid'] )

         #if ip_internet:
         #   zapi.usermacro.create({
         #       "hostid": hostid,
         #       "macro": "{$IP_INTERNET}",
         #       "value": ip_internet
         #  }) 
