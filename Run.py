import copy
from Cuadrupla import Cuadrupla
dicFuncionQuick={
    'Minimo': [['int'], 12], 
    'Ordenar':[[], 16], 
    'OutputInt': [[], 4], 
    'InputInt': [['int'], 0], 
    'main': [[], 4]
    }

dicFuncionFactorial={
    'factorial': [['int'], 4], 
    'OutputInt': [[], 4], 
    'InputInt': [['int'], 0], 
    'main':[[], 4]
    }

dicFuncionFibo={
    'OutputInt':[[], 4],
    'InputInt': [['int'], 0],
    'fib': [['int', 'int'], 16],
    'main': [[],12]
    }

dicFuncionAker={'OutputInt':  [[], 4], 
 'InputInt':  [['int'], 0], 
 'Ackerman': [['int', 'int', 'int'], 8], 
 'main':  [[], 8]}   

import pickle
from Assembler import *
#infile = open("cuadruplas_factorial",'rb')
infile = open("cuadruplas_aker",'rb')
#infile = open("cuadruplas_fibo",'rb')
# infile = open("cuadruplas_quick",'rb')
codigoIntermedio2 = pickle.load(infile)
infile.close()
main=[]
funcs=[]
temp=[]
def RUN(main, funcs):
    #mips = Assembler(dicFuncionFibo)
    #mips = Assembler(dicFuncionFactorial)
    mips = Assembler(dicFuncionAker)
    # mips = Assembler(pilaFuncionFactorial)
    mips.header(40)
    mips.makeMIPS(main)
    mips.final()
    mips.makeMIPS(funcs)
    pass

for linea in codigoIntermedio2:
    temp.append(linea)
    if(linea.op == 'END FUNCTION'):
        if(temp[0].arg1 == 'main'):
            main += copy.deepcopy(temp)
        else:
            funcs += copy.deepcopy(temp)
        temp = []
print("###############MAIN###############")
print(main)
print("###############Metodos###############")
print(funcs)
RUN(main, funcs)