import copy
class RegisG:
    def __init__(self):
        self.Lregs = {'$t1': [],'$t2': [],'$t3': [],'$t4': [],'$t5': [],'$t6': [],'$t7': [],'$t8': [],'$t9': [],}
        self.acces = {}
    #Se agregan los registros dependiendo del tipo que sea
    def appR(self, var):
        if(var == 'R'):
            return
        try:
            var = int(var)
            return
        except:
            if var not in self.acces.keys():
                if (var.find('fp') != -1):
                    self.acces[var] = [var]
                elif (var.find('G') != -1):
                    self.acces[var] = [var]
                else:
                    self.acces[var] = []
    #ayuda para poder encontrar los registros a asignar
    def getReg2(self, var, x=None, full=[]):
        if ( len(self.acces[var]) > 0):
            reg2 = self.findReg(var)
            if reg2:
                return reg2
        reg2 = self.findRegEmp()
        if reg2:
            self.LD1(reg2, var)
            return reg2
        dTemp = None
        if x :
            dTemp = self.delTempX(x)
        else:
            dTemp = copy.deepcopy(self.Lregs)
        reg2 = self.findRegEmp(dTemp)
        if reg2 :
            if not reg2 in full:
                self.LD1(reg2, var)
                return reg2
        reg2 = self.RegSpace(dTemp, full)
        if reg2:
            self.LD1(reg2, var)
            return reg2
        reg2 = self.choiceReg(dTemp, full)
        self.ST2(reg2)
        self.LD1(reg2, var)
        return reg2
    #Se eliminan lo que se agrego de forma temporal
    def delTemp(self, temp):
        try:
            temp = int(temp)
            return
        except:
            pass
        if temp.find('t') == -1:
            return
        for i in self.acces[temp]:
            try:
                self.Lregs[i].remove(temp)
            except:
                continue
        del self.acces[temp]
    #se limpian todos los registros
    def clenDesc(self):
        for key in self.Lregs.keys():
            self.Lregs[key] = []
        self.acces = {}
    #se elimina la variable de un registro
    def cleanVarDer(self, var):
        for key, value in self.Lregs.items():
            try:
                value.remove(var)
            except:
                continue
    #sirve para poder guardar los registros en el stack
    def ST1(self, x, R):
        print(f'ST {x}, {R}')
        self.cleanVarDer(x)
        self.acces[x] = [x]
    def ST2(self, R):
        for var in self.Lregs[R]:
            self.ST1(var, R)
    #sirve para buscar el registro dependiendo de la variable
    def findReg(self, var):
        for i in self.acces[var]:
            if (i.find('$t') != -1):
                return i
    #sirve para poder buscar un registro disponible
    def findRegEmp(self, Lregs=None):
        if (not Lregs):
            Lregs = copy.deepcopy(self.Lregs)
        for key, value in Lregs.items():
            if (len(value) == 0):
                return key
    #Sirve para poder crear registros sin variables
    def delTempX(self, var):
        dTemp = {}
        for key, value in copy.deepcopy(self.Lregs.items()):
            try:
                dTemp[key] = value.remove(var)
            except:
                continue
        return dTemp
    #Obtiene la cantidad de registros actuales
    def countReg(self, var):
        regs = []
        for i in self.acces[var]:
            if (i.find('R') != -1):
                regs.append(i)
        return regs
    #Sirve para poder cargar los registros en el stack
    def LD1(self, R, x):
        if x.find('t') == -1:
            if x.find('fp') != -1:
                offset = x[x.find('[') + 1:x.find(']')]
                print(f'\tlw {R}, {offset}($fp)')
        self.Lregs[R] = [x]
        self.acces[x].append(R)
    #Busca los registros que tienen una sola variable
    def RegSpace(self, Lregs, full):
        for key, value in Lregs.items():
            if len(value) == 1:
                regs = self.countReg(value[0])
                if len(regs) > 2:
                    regs.remove(key)
                    if regs[0] in full:
                        continue
                    return regs[0]
    #Sirve para poder buscar el mejor registro para liberar
    def choiceReg(self, Lregs, full):
        fnd = sorted(
            Lregs.items(), key=lambda x: len(x[1]), reverse=False)
        for i in fnd:
            if i[0] not in full:
                return i[0]
    #Es la funcion encargada de poder designar los registros para trabajar.
    def getReg(self, x, y, z=None):
        regs = []
        ops = None
        if (z == None):
            if (x == y):
                ops = x
            Lregs = self.getReg2(y, ops, regs)
            regs.append(Lregs)
            regs.append(Lregs)
        else:
            if (x == y or x == z):
                ops = x
            for var in [x, y, z]:
                if(var == 'R'):
                    continue
                try:
                    var = int(var)
                    continue
                except:
                    regs.append(self.getReg2(
                        var, ops, regs))
        return regs
