from subprocess import Popen
var1 = 0
var2 = 0
var3 = 0
Process = Popen(['./test.sh %s %s %s'%(str(var1),str(var2),str(var3))],shell=True)
