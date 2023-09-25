import numpy as np
from math import *

def Based(x,deltax,*args):            # Função para formatar os números + as suas incertezas
    deltax=abs(deltax)
    if deltax < abs(x*10**-18):
        deltax=0
    
    Negative = 0
    if x<0:
        Negative = 1
        
    Origin=[x,deltax]                  
    x=f"{x:.325e}"
    x=x.split("e")
    deltax=f"{deltax:.325e}"
    
    Origin.append(x)  
    
    dList=[]
        
    for i in deltax:
        if (i == "0" or i == "." or i == "e" or i == "+" or i == "-"):
            if len(dList)>0 and i == "0":
                dList.append(i)
        else:
            dList.append(i)
        if len(dList)>=4:
            break
        
        
    if len(dList)>=1:
        if int(dList[0]+dList[1]) >= 35:
            error=int(round(float(dList[0]+"."+dList[1]+dList[2]+dList[3]),0))
        else:
            error=int(round(float(dList[0]+dList[1]+"."+dList[2]+dList[3]),0))
    else:
        error=0
                
    deltax=deltax.split("e")
    
    if float(deltax[0])< round(float(deltax[0]),0) and deltax[0][0] == '9':  # Correção do Bug encontrado
        deltax[1]=str(int(deltax[1])+1)
        
    ExtraDec=len(str(error))-1
    
    save=int(x[1])-int(deltax[1])+ExtraDec
    
    if save<0:
        raise ValueError(f'Error bigger than value. {Origin[1]:.2e} >> {Origin[0]:.2e}')
    
    try:
        xprime=f"{round(float(x[0][0:save+4+Negative:1]),save):.{save}f}e{x[1]}"
        var=len(str(float(xprime)))-len(f"{float(xprime):.{save-int(x[1])}f}")
    except:
        var=1
    
    if Origin[1]<=35*abs(Origin[0]):
        if error!=0:
            if abs(int(Origin[2][1]))<3 and var==0:
                result=f"{float(xprime):.{save-int(x[1])}f}({error})"
            else:
                result=f"{round(float(x[0][0:save+4+Negative:1]),save):.{save}f}({error})e{x[1]}"
        else:                                                          
            if abs(int(Origin[2][1]))<3:
                result=f"{Origin[0]:f}"
            else:
                result=f"{Origin[0]:e}"
    else:
        if int(deltax[1])<0 and abs(int(deltax[1]))<3:
            zeros="0."
            for i in range(abs(int(deltax[1]))+ExtraDec):
                zeros=zeros+"0"
            result=f"{zeros}({error})"
        else:
            result=f"0 ± ({Origin[1]:.1e})"
        
    return f"\nYour Math Input = {result}"

#################################################################################################

def deri(Func,a,b,*args,Step=0.0001,):    # Derivada com 3 pontos
    DefaultStep = 0.0001
    if Step <= DefaultStep:
        Step = DefaultStep
    if a > (10**16*Step):
        raise ValueError("The Computer is Lacking The Precision To Compute The Derivative")
    Interval = np.arange(round(a-Step,16),round(b+2*Step,16),Step)
    Size= b-a
    Partitions = round((Size / Step),0)
    if (b-a) < Step:
        Partitions+=1
    Counter = 0
    FD3=[]
    while Counter < Partitions:
        Fk_m1=Func(Interval[Counter],args)
        Fk_p1=Func(Interval[Counter+2],args)
        Counter+=1
        FD3.append((Fk_p1-Fk_m1)/(2*Step))
    return FD3[-1]
    
def Fadd(x,*args):
    y=0
    if len(args[0])>0:
        y=args[0][0]
    return x + y

def Fmul(x,*args):
    y=1
    if len(args[0])>0:
        y=args[0][0]
    return x*y
    
def Fdis(x,*args):
    y=1
    if len(args[0])>0:
        y=args[0][1]
    if args[0][0] == 'x':
        return x/y
    if args[0][0] == 'y':
        return y/x
    
def Fpow(x,*args):
    y=1
    if len(args[0])>0:
        y=args[0][1]
    if args[0][0] == 'x':
        return x**y
    if args[0][0] == 'y':
        return y**x

def Flog(x,*args):
    if x>0:
        return log(x)
    else:
        raise ValueError(f"log({x}) has not been defined")
   
    

def exp(*args):
    StringText=args[0]
    Hold=["x","y","z","k","l","m","n"]
    Variable=args[1::][0]

    for i in range(len(Hold)):
        try:
            locals()[f'{Hold[i]}']=Variable[0][i]
        except:
            break
    return eval(StringText)

def Properror(Type,func,*args): # Função para propagar os erros
    deri=args[0][0]
    args=args[0][1:]
    if Type == 'mul':
        return ((deri(func,args[0][0],args[0][0],Step=args[0][1])*args[0][1]*args[1][0])**(2)+(deri(func,args[1][0],args[1][0],Step=args[1][1])*args[1][1]*args[0][0])**(2))**(1/2)
    if Type == 'add':
        return ((deri(func,args[0][0],args[0][0],Step=args[0][1])*args[0][1])**(2)+(deri(func,args[1][0],args[1][0],Step=args[1][1])*args[1][1]**(2)))**(1/2)
    if Type == 'div':
        return ((deri(func,args[0][0],args[0][0],'x',args[1][0],Step=args[0][1])*args[0][1])**(2)+(deri(func,args[1][0],args[1][0],'y',args[0][0],Step=args[1][1])*args[1][1])**(2))**(1/2)
    if Type == 'pow':
        return ((deri(func,args[0][0],args[0][0],'x',args[1][0],Step=args[0][1])*args[0][1])**(2)+(deri(func,args[1][0],args[1][0],'y',args[0][0],Step=args[1][1])*args[1][1])**(2))**(1/2)
    if Type == 'log':
        if args[0][0] > 0:
            return ((deri(func,args[0][0],args[0][0])*args[0][1])**(2))**(1/2)
    else:
        raise ValueError(f"log({args[0][0]}) has not been defined")


################################################################################################


class FNum:  # Class

    def __init__(self,Value,Error):
        self.Value=Value
        self.Error=Error
    
    def value(self):
        return self.Value
    
    def error(self):
        return self.Error
    
    def NewError(self,other):  # Alterar o erro depois de já ter sido definido
        other=float(other)
        return FNum(self.Value,other)
    
    def __int__(self):
        return int(self.Value)
    
    def __float__(self):
        return float(self.Value)
    
    def __neg__(self):
        return FNum(-self.Value,self.Error)
        
########################################################################################## 
    
    def function (self,f, *args):
        return f(args[0],args[1],args[2::])
    
    def __add__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
            other=FNum(other,0)
        NewValue=self.Value+other.Value
        Error = self.function(Properror,'add',Fadd,deri,(self.Value,self.Error),(other.Value,other.Error))
        return FNum(NewValue,Error)
    
    def __radd__(self,other):
        return self+other
    
    def __sub__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
            other=FNum(other,0)
        temp=FNum(-other.Value,other.Error)
        return self+temp
    
    def __rsub__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
            other=FNum(other,0)
        temp=FNum(-self.Value,self.Error)
        return temp+other
        
    def __mul__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
            other=FNum(other,0)
        NewValue=self.Value*other.Value
        Error = self.function(Properror,'mul',Fmul,deri,(self.Value,self.Error),(other.Value,other.Error))
        return FNum(NewValue,Error)
    
    def __rmul__(self,other):
        return self*other
    
    def __truediv__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
           other=FNum(other,0)
        NewValue=self.Value/other.Value
        Error = self.function(Properror,'div',Fdis,deri,(self.Value,self.Error),(other.Value,other.Error))
        return FNum(NewValue,Error)
    
    def __rtruediv__(self,other):
        return self/other
    
    def __pow__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
           other=FNum(other,0)
        NewValue=self.Value**other.Value
        Error = self.function(Properror,'pow',Fpow,deri,(self.Value,self.Error),(other.Value,other.Error))
        return FNum(NewValue,Error)
        pass
    
    def __rpow__(self,other):
        return pow(self,other)
    
    def log(self):          # log base e
        if self.Value > 0:
            NewValue=log(self.Value)
        else:
            raise ValueError(f"log({self.Value}) has not been defined")
        Error = self.function(Properror,'log',Flog,deri,(self.Value,self.Error))
        return FNum(NewValue,Error)
    
    def expression(expression,*args):
        return exp(expression,args)

###############################################################################################
    
    def __eq__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
           other=FNum(other,0)
        deltax=self.Error
        deltay=other.Error
        deltaf=((deltax**2+((-1)*deltay)**2)**(1/2))
        value = self.Value - other.Value
        if abs(value) <= deltaf :
            return True
        else:
            return False
        
    def __ne__(self,other):
        return not self==other
    
    def __gt__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
           other=FNum(other,0)
        if self!=other:
            if self.Value>other.Value:
                return True
            else:
                return False
        else:
            return False
            
    def __lt__(self,other):
        if type(other)!=type(self) and type(other)!=type(str):
           other=FNum(other,0)
        if self!=other:
            if self.Value<other.Value:
                return True
            else:
                return False
        else:
            return False
            
    def __ge__(self,other):
        return not self<other
    
    def __le__(self,other):
        return not self>other
    
#######################################################################################
    
    def __str__(self):
        return self.function(Based,self.Value,self.Error) 
    
    def __repr__(self):
        return (self.Value,self.Error)
    
   
#######################################################################################    
   
def Print(Hold_List):
    print("This Program allows you to compute simple calculations with errors associated to the varaibles\n"
          "To use the fuction log please use the format (Math Expression Inside The Log).log()\n"
          "\nAn Example Of A Possible Expression :  x**2 == (2*x*y)/((z**(k+l)).log()-1)\n")
    globals()['Hold']=Hold_List
    print(f'Hold = {Hold}')
    return    

def Run():        # Função para executar o programa
    Variables=[]
    VariableNumber=int(input("\nNumber Of Variables = "))
    
    Hold_List = []
    
    for _ in range(VariableNumber):
        Hold_List.append(str(input(f"Variable {_+1} Name = ")))
        
    Print(Hold_List)
    
    ErrorON=input("Variables with Errors ON = ")
    if ErrorON == 'True':
        for i in range(VariableNumber):
            locals()[f'{Hold[i]}']=FNum(float(input(f'\n{Hold[i]} = ')),float(input(f'{Hold[i]} Error = ')))
            Variables.append(eval(f'{Hold[i]}'))
    elif ErrorON == 'False':
        for i in range(VariableNumber):
            locals()[f'{Hold[i]}']=FNum(float(input(f'\n{Hold[i]} = ')),0)
            Variables.append(eval(f'{Hold[i]}'))
    else:
        print("--- Assuming Errors = False ---")
        for i in range(VariableNumber):
            locals()[f'{Hold[i]}']=FNum(float(input(f'\n{Hold[i]} = ')),0)
            Variables.append(eval(f'{Hold[i]}')) 
    
        
    Exp = input("\nPlease Type Your Expression\n\n")    
    result=FNum.expression(Exp,Variables)
    if type(result)!=type(FNum(0,0)):
        print(f"\nYour Math Input = {result}")
    else:
        print(f"\n{result}")
    if input("\nType 'Exit' to Close or press Enter to continue\n") == 'Exit':
        return False
    return True


if __name__ == '__main__':
    Running=True
    while Running:
        Running = Run()

