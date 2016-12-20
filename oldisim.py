# coding: utf-8

# Este script lanza otros (bash) scripts para provisionar una máquina, 
# ejecutar en ella tres veces el benchmark oldisim
# y mover los resultados json a la carpeta oportuna, tras lo que
# desmantela la máquina

# En los tipos de instancia elimino las de 8 cores, porque, al instanciar
# 3 de cada una, me saldrían 8x3 = 24 lo que excede la quota de 20 cores por region

instance_types_to_test = [
#      # 'Basic_A0', 
#      'Basic_A1', 'Basic_A2', # u'Basic_A3', # u'Basic_A4', 
#      'ExtraSmall', 'Large', 'Medium', 'Small', # "ExtraLarge"
#      "A5", "A6",   # "A7"
#      "Standard_D1", "Standard_D2",  "Standard_D3", # "Standard_D4", 
#      "Standard_D11", "Standard_D12", # "Standard_D13", "Standard_D14", 
#      "Standard_D1_v2", "Standard_D2_v2", "Standard_D3_v2", # "Standard_D4_v2", 'Standard_D5_v2',
       'Standard_D11_v2','Standard_D12_v2', # 'Standard_D13_v2', 'Standard_D14_v2' 
     ]


import commands
from datetime import datetime
import sys
import re
for i in instance_types_to_test:

    # Provision
    t1 = datetime.now()
    print("Provisionando máquina tipo %s" % i)
    l = commands.getstatusoutput("./oldi-provisionar %s" % i)
    print("Terminado en %s" % (datetime.now()-t1))
    if l[0]!=0:
        print("ERROR al provisionar máquina tipo %s" % i)
        print(l[1])
        sys.exit(-1)
    m=re.search('--run_uri=(\w+)',l[1])
    if not m:
        print("ERROR, no puedo encontrar el run_uri")
        sys.exit(-1)
    else:
        print("run_uri: %s" % m.groups())
        run_uri = m.groups()[0]

    # Preparacion
    t1 = datetime.now()
    print("Preparando el software necesario...")
    l = commands.getstatusoutput("./oldi-preparar %s" % run_uri)
    print("Terminado en %s" % (datetime.now()-t1))
    if l[0]!=0:
        print("ERROR al preparar máquina tipo %s" % i)
        print(l[1])
        sys.exit(-1)

    # Benchmark
    t1 = datetime.now()
    print("Ejecutando benchmarks...")
    l = commands.getstatusoutput("./oldi-run %s" % run_uri)
    print("Terminado en %s" % (datetime.now()-t1))
    if l[0]!=0:
        print("ERROR al ejecutar benchmarks")
        print(l[1])
        sys.exit(-1)

    # Desmantelar
    t1 = datetime.now()
    print("Desmantelando máquina tipo %s" % i)
    l = commands.getstatusoutput("./oldi-teardown %s" % run_uri)
    print("Terminado en %s" % (datetime.now()-t1))
    if l[0]!=0:
        print("ERROR al desmantelar máquina tipo %s" % i)
        print(l[1])
        sys.exit(-1)

    # Renombrar resultados
    file_in  = "results-%s.json" % run_uri
    file_out = "oldisim-%s.json" % i
    print("Guardando resultados en %s" % file_out)
    l = commands.getstatusoutput("mv %s %s" % (file_in, file_out))
    if l[0]!=0:
        print("ERROR al renombrar fichero")
        print(l[1])
        sys.exit(-1)
