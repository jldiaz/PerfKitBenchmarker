#coding: utf-8

# Este script usa el comando `azure` para listar los identificadores
# de cada posible tipo de máquina, en las regiones que azure considera

import commands

j = commands.getstatusoutput("azure vm location list --json")[1]

import json
data = json.loads(j)

import pprint
for region in data:
    print(region["name"])
    print(region["computeCapabilities"]["virtualMachinesRoleSizes"])
    print("-"*80)

