from RegisG import *

class Assembler:
    def __init__(self, dictCF):
        self.paramF = dictCF
        self.lrParam = ['$a0', '$a1', '$a2', '$a3']
        self.generator = RegisG()
    def makeMIPS(self, quads):
        func = ""
        for i in quads:
            if i.op == 'FUNCTION':
                print(f"{i.arg1}:")
                self.seestack(i.arg1)
                func = i.arg1
                if(i.arg1 == 'InputInt'):
                    self.Inputs()
                elif(i.arg1 == 'OutputInt'):
                    self.Outputs()
                continue
            elif i.op == 'RETURN':
                if (func == 'InputInt'):
                    print('\tjr $ra')
                    self.lrParam = ['$a0', '$a1', '$a2', '$a3']
                else:
                    self.retuns(i.arg1, func)
                continue
            elif i.op == 'END FUNCTION':
                func = ""
                self.generator.clenDesc()
                continue
            elif i.op == 'CALL':
                self.saveState()
                print(f"\tjal {i.arg1}")
                self.lrParam = ['$a0', '$a1', '$a2', '$a3']
                continue
            elif i.op == 'PARAM':
                self.paramss(i.arg1)
                continue
            elif i.op.find('LABEL') != -1:
                self.saveState()
                print(f"{i.op}:")
                continue
            elif(i.op == 'GOTO'):
                self.saveState()
                print(f"\tj {i.arg1}\n")
                continue
            elif i.op == '+':
                self.operators(i,i.op)
                continue
            elif i.op == '-':
                self.operators(i,i.op)
                continue
            elif i.op == '*':
                self.operators(i,i.op)
                continue
            elif i.op == '=':
                self.equals(i)
                continue
            elif(i.op == '<'):
                self.operators(i,i.op)
                continue
            elif(i.op == '<='):
                self.operators(i,i.op)
            elif(i.op == '=='):
                self.operators(i,i.op)
                continue
            elif(i.op == 'IF'):
                self.saveState()
                self.ifs(i)
                continue
            else:
                pass
    #carga los datos del stack
    def loadStack(self, name):
        vals = self.paramF[name][1]
        if(vals != 0):
            print(f'''
\tadd $sp, $fp, {vals}
\tlw $fp, ($sp)
\tadd $sp, $sp, 4
\tlw $ra, ($sp)
\tadd $sp, $sp, 4
                ''')
    #busca los valores que queremos del stack
    def seestack(self, name):
        if (name == 'main'):
            vals = self.paramF[name][1]
            print(f'''
\tla $s7, G''')
            if(vals != 0):
                print(f'''
\tsw $fp, ($sp)
\tsub $fp, $sp, {vals}
\tla $sp, ($fp)
                ''')
        elif (name != 'OutputInt'):
            vals = self.paramF[name][1]
            if(vals != 0):
                print(f'''
\tsub $sp, $sp, 4
\tsw, $ra, ($sp)
\tsub $sp, $sp, 4
\tsw $fp, ($sp)
\tsub $fp, $sp, {vals}
\tla $sp, ($fp)
                ''')
                if(len(self.paramF[name][0]) > 0):
                    self.saveStack(
                        len(self.paramF[name][0]))
    #Se guardan en stack los parametros de la funcion
    def saveStack(self, cParam):
        rParams = ['$a0', '$a1', '$a2', '$a3']
        for i in range(cParam):
            print(f"\tsw {rParams.pop(0)}, {4 * i}($fp)")
    #sirve para poder ver el parametro que se pide
    def paramss(self, param):
        try:
            param = int(param)
            print(f"""
\tli {self.lrParam.pop(0)}, {param}""")
            return
        except:
            pass
        if (param[0] == 't'):
            reg = self.generator.findReg(param)
            print(f"""
\tmove {self.lrParam.pop(0)}, {reg}""")
        elif (param.find('fp') != -1):
            offset = param[param.find('[') + 1:param.find(']')]
            print(f"""
\tlw {self.lrParam.pop(0)}, {offset}($fp)""")
        elif(param == 'R'):
            print(f"""
\tmove {self.lrParam.pop(0)}, $v0""")
        elif(param.find('G') != -1):
            offset = param[param.find('[') + 1:param.find(']')]
            if (offset.find('t') != -1):
                reg = self.generator.findReg(offset)
                print(f'''
\tadd $s3, {reg}, $s7
\tlw $s0, ($s3)
\tmove {self.lrParam.pop(0)}, $s0
            ''')
                self.generator.delTemp(offset)
            else:
                print(f"""
\tlw $s0, {offset}($s7)
\tmove {self.lrParam.pop(0)}, $s0""")
    #Genera el mips de cuando se quiere comparar algo
    def equals(self, quad):
        val1 = quad.resultado
        val2 = quad.arg1
        if ((val2 == 'R') and (val1.find('fp') != -1)):
            offset = val1[val1.find('[') + 1:val1.find(']')]
            print(f"\tsw $v0, {offset}($fp)")
        elif (val1.find('fp') != -1):
            offset = val1[val1.find('[') + 1:val1.find(']')]
            try:
                val2 = int(val2)
                print(f'''\tli $s5, {val2}
\tsw $s5, {offset}($fp)
                ''')
            except:
                if(val2.find('G') != -1):
                    val2 = val2[val2.find('[') + 1:val2.find(']')]
                regs = self.generator.getReg(val1, val2)
                print(f"\tsw {regs[0]}, {offset}($fp)")
                self.generator.delTemp(val2)
        elif(val1.find('G') != -1):
            offset = val1[val1.find('[') + 1:val1.find(']')]
            try:
                val2 = int(val2)
                if (offset.find('t') != -1):
                    reg = self.generator.findReg(offset)
                    print(f'''\tli $s5, {val2}
\tadd $s3, {reg}, $s7
\tsw $s5, ($s3)
                    ''')
                    self.generator.delTemp(offset)
                else:
                    print(f'''\tli $s5, {val2}
\tsw $s5, {offset}($s7)
                    ''')
            except:
                if((val1.find('G') != -1) and val2[0] == 't'):
                    offset = val1[val1.find('[') + 1:val1.find(']')]
                    reg = self.generator.findReg(val2)
                    try:
                        offset = int(offset)
                        print(f'''
\tsw {reg}, {offset}($s7)
                        ''')
                        self.generator.delTemp(val2)
                    except:
                        pass
                pass
    #genera el codigo cuando hay ifs
    def ifs(self, quad):
        temp = quad.arg1[:quad.arg1.find('>')]
        self.generator.appR(temp)
        reg = self.generator.getReg(temp, temp)
        name = quad.resultado
        print(f'''
\tbgtz {reg[0]}, {name}
        ''')
        self.generator.delTemp(temp)
    #genra los valores de retorno de las funciones
    def retuns(self, reg, name):
        if (reg != 'R'):
            try:
                srts = int(reg)
                print(f'\tli $v0, {srts}')
            except:
                if(reg.find('fp') != -1):
                    offset = reg[reg.find('[') + 1:reg.find(']')]
                    print(f'\tlw $v0, {offset}($fp)')
                    return
                reg = self.generator.findReg(reg)
                print(f'\tmove $v0, {reg}')
        self.loadStack(name)
        print("\tjr $ra")
        self.lrParam = ['$a0', '$a1', '$a2', '$a3']
    def Outputs(self):
        print('''
\tli $v0, 1
\tsyscall
\tli $v0, 4
\tla $a0, jumpL
\tsyscall
\tjr $ra
        ''')
    def Inputs(self):
        print('''
\tli $v0, 4
\tla $a0, msg
\tsyscall
\tli $v0,5
\tsyscall
\tjr $ra
        ''')
    #Salva el estado antes de cambiar a funcion 
    def saveState(self):
        for i in self.generator.acces:
            if(i.find('fp') != -1):
                offset = i[i.find('[') + 1:i.find(']')]
                print(
                    f"\tsw {self.generator.findReg(i)}, {offset}($fp)")
        self.generator.clenDesc()
    #crea el encabezado de MIPS
    def header(self, espacioGlobal):
        newLine = "\n"
        print(f'''
.data
.align 2
    G: .space {espacioGlobal}
    msg: .asciiz "Enter Value: "
    jumpL: .asciiz "{repr(newLine).replace("'","")}"
.text
        ''')
    #Crea el final de MIPS
    def final(self):
        print('''
\tli $v0, 10
\tsyscall
        ''')
    #genera el mips dependiendo del operador.
    def operators(self, quad,op):
        val1 = quad.resultado
        val2 = quad.arg1
        val3 = quad.arg2
        self.generator.appR(val1)
        self.generator.appR(val2)
        self.generator.appR(val3)
        compr = 0
        srts = None
        try:
            val2 = int(val2)
            compr = 1
            srts = val2
        except:
            pass
        try:
            val3 = int(val3)
            compr = 1
            srts = val3
        except:
            pass
        regs = self.generator.getReg(val1, val2, val3)
        if op=="*":
            if(compr==1):
                print(f'''
    \tli $s5, {srts}
    \tmul {regs[0]}, {regs[1]}, $s5
                ''')
            elif(val3 == 'R'):
                print(f'''
    \tmul {regs[0]}, {regs[1]}, $v0
                ''')
        elif op=="+":
            if(compr==1):
                print(
                    f"\taddi {regs[0]}, {regs[1]}, {srts}")
            else:
                print(f"\tadd {regs[0]}, {regs[1]}, {regs[2]}")
        elif op=="-":
            if(compr==1):
                print(f'''
    \tli $s5, {srts}
    \tsub {regs[0]}, {regs[1]}, $s5 
                ''')
        elif op=="==":
            if (compr==1):
                print(f'''
    \tli $s5, {srts}
    \tseq {regs[0]}, {regs[1]}, $s5 
                ''')
        elif op=="<='":
            if (compr==1):
                print(f'''
    \tli $s5, {srts}
    \tsle {regs[0]}, {regs[1]}, $s5 
                ''')
        elif op=="<":
            if (compr==1):
                print(f'''
    \tli $s5, {srts}
    \tslt {regs[0]}, {regs[1]}, $s5 
                ''')
        self.generator.delTemp(val2)
        self.generator.delTemp(val3)
