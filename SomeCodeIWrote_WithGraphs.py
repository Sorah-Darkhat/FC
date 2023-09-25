import numpy as np
import matplotlib.pyplot as plt
from pip._vendor import requests
from scipy.stats import t
import os
#from scipy.stats import linregress

cwd = os.getcwd()

os.makedirs(f'{cwd}/GraphsFolder', exist_ok=True)

def Based(x,deltax,*args):
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
        
    return f"\na ± ∆a = {result}"        # Modded to print a instead of x

def PivotMaker(Matrix,iteration,Vector=[]):
    col=iteration
    ColValues=[]
    for line in range(len(Matrix[iteration::])):
        ColValues.append(abs(Matrix[line+iteration][col]))
    Max=0
    for Value in ColValues:
        if Value>Max:
            Max=Value
    Index=ColValues.index(Max)+iteration
    Temp1=list(Matrix[iteration])
    if np.ndim(Vector)>=2:
        Temp2=list(Vector[iteration])
    else:
        Temp2=Vector[iteration]
    Matrix[iteration]=Matrix[Index]
    Vector[iteration]=Vector[Index]
    Matrix[Index]=np.array(Temp1,dtype=float)
    Vector[Index]=Temp2
    
    return Matrix,Vector
                        

def Gauss(Matrix,Vector,Pivot):
    if np.ndim(Vector)==1:
        for i in range(len(Matrix)):
            if abs(Matrix[i][i])>0 and not Pivot:
                for j in range(i+1,len(Matrix)):
                    CALC=Matrix[j][i]/Matrix[i][i]
                    for iteration in range(len(Matrix)):
                        Matrix[j][iteration]=Matrix[j][iteration]-CALC*Matrix[i][iteration]
                    Vector[j]=Vector[j]-CALC*Vector[i]
            elif not Pivot:
                raise ValueError("Zero Divion")
            else:
                Matrix,Clear=PivotMaker(Matrix,i,Vector)
                for j in range(i+1,len(Matrix)):
                    CALC=Matrix[j][i]/Matrix[i][i]
                    for iteration in range(len(Matrix)):
                        Matrix[j][iteration]=Matrix[j][iteration]-CALC*Matrix[i][iteration]
                    Vector[j]=Vector[j]-CALC*Vector[i]
    elif np.ndim(Vector)>=2:
        for i in range(len(Matrix)):
            if abs(Matrix[i][i])>0 and not Pivot:
                for j in range(i+1,len(Matrix)):
                    CALC=Matrix[j][i]/Matrix[i][i]
                    for iteration in range(len(Matrix)):
                        Matrix[j][iteration]=Matrix[j][iteration]-CALC*Matrix[i][iteration]
                        Vector[j][iteration]=Vector[j][iteration]-CALC*Vector[i][iteration]
            elif not Pivot:
                raise ValueError("Zero Divion")
            else:
                Matrix,Vector=PivotMaker(Matrix,i,Vector)
                for j in range(i+1,len(Matrix)):
                    CALC=Matrix[j][i]/Matrix[i][i]
                    for iteration in range(len(Matrix)):
                        Matrix[j][iteration]=Matrix[j][iteration]-CALC*Matrix[i][iteration]
                        Vector[j][iteration]=Vector[j][iteration]-CALC*Vector[i][iteration]
    return Matrix,Vector


def MSolver(Matrix,Vector,Pivot):
    Matrix,Vector=Gauss(Matrix,Vector,Pivot)
    Variables={}
    for i in range(len(Matrix)):
        i='x'+str(len(Matrix)-i)
        for j in range(len(Variables.keys())+1):
            Sub=0
            for key in Variables:
                value=Variables[key]
                TM=key.split('x')
                TM=TM[1]
                Sub+=Matrix[int(-1)-int(j)][int(TM)-1]*value
            Result=(Vector[-1-j]-Sub)/Matrix[-1-j][-1-j]
            Variables[i]=Result
               
    HoldList=[]
    Var={}
    for key in Variables:
        HoldList.append((key,Variables[key]))
    for i in range(len(HoldList)):
        Temp=HoldList[-1-i]
        HoldList[-1-i]=HoldList[i]
        HoldList[i]=Temp
    for elem in HoldList:
        Var[elem[0]]=elem[1]
    
    return Var


def Madjust(points,Level,Xn,Yn,Step=0.1,Line=False,All=False):
    X=[x[0] for x in points]
    Y=[y[1] for y in points]
    
    Sums={}
    Vecs={}
    Strings=[]
    Strings2=[]
    
    for i in range(2*Level+1):
        string=f'x{i}'
        Strings.append(string)
        Strings2.append('y'+string)
        
    for i in range(len(Strings)):
        Sums[Strings[i]]=0
        Vecs[Strings2[i]]=0
        
    for key in Sums:
        ep=int(key.split('x')[-1])
        Values=[]
        Values2=[]
        for value in points:
            Values.append(value[0]**(ep))
            Values2.append(value[0]**(ep)*value[1])
        Sums[key]=sum(Values)
        Vecs['y'+key]=sum(Values2)
        
    
    Lines=[]
    for i in range(Level+1):
        line=[]
        for j in range(i,Level+1+i):
            line.append(Sums[f'x{j}'])
        Lines.append(line)
    
    V=[]
    for i in range(Level+1):
        V.append(Vecs['yx'+f'{i}'])
        
    Lines=np.array(Lines,dtype=float)
    Vec=np.array(V,dtype=float)
    Pol=MSolver(Lines,Vec,True)
    
    Lilith=[]
    for key in Pol:
        Val='x'+str(int((key.split('x')[-1]))-1)          
        Lilith.append((Val,Pol[key]))
    
    ming=''
    for polv in Lilith:
        nep=int(polv[0].split('x')[-1])
        if str(polv[1])[0] == '-':
            if nep >1:
                ming += f' - {str(polv[1])[1::]}*x**{nep}'
            elif nep>0:
                ming += f' - {str(polv[1])[1::]}*x'
            else:
                ming += f' - {str(polv[1])[1::]}'
        else:
            if nep >1:
                ming += f' + {polv[1]}*x**{nep}'
            elif nep>0:
                ming += f' + {polv[1]}*x'
            else:
                ming += f' + {polv[1]}'
                
    if ming[1]=='+':
        ming=ming[2::]

    vi=min(X)-abs(min(X)/20)
    vo=max(X)+abs(max(X)/20)

    if not All:
        print(f"-------------------------------------------\n\nFor Level = {Level}\n\nf(x) ={ming}\n")

    if Line == False:
        NX=[vi+i*Step for i in range(int(round((vo/Step),0)+1))]
        NY=[eval(ming) for x in NX]
    else:
        NX=[vi,(vo+vi)/(2),vo]
        NY=[eval(ming) for x in NX]
    
    ys=[]
    mys=[]
    for value in points:
        x=value[0]
        y=value[1]
        ys.append(y)
        my = eval(ming)
        mys.append(my)

    Diff=np.sum( (np.array(ys,dtype=float) - np.array(mys,dtype=float) ) ** 2 )
    return Diff/(len(points)-Level-1),ming,(X,Y,NX,NY)



def Cor(points,X,Y,Level=1,Allpass=False):
    C=Madjust(points,Level,X,Y,Step=0.01,Line=True,All=Allpass)
    dif=(C[0])**(1/2)
    if not Allpass:
        print(f"-------------------------------------------\n")
    a=(C[1].split('*'))[0]
    stra=''
    for char in a:
        if char == ' ':
            pass
        else:
            stra+=char
    a=float(stra)
    x=[]
    y=[]
    for xy in points:
        x.append(xy[0])
        y.append(xy[1])
   
    n=len(points)
        
    x=np.array(x,dtype=float)
    y=np.array(y,dtype=float)
    
    x2=np.sum(x**2)
    xS=(np.sum(x))**2
    
    y2=np.sum(y**2)
    yS=(np.sum(y))**2
    
    xSum=np.sum(x)
    ySum=np.sum(y)
    xySum=np.sum(x*y)
    
    Fra=n*xySum-xSum*ySum
    tion=((n*x2-xS)**(1/2)*(n*y2-yS)**(1/2))**(-1)
    Fraction=Fra*tion
    
    if a>0:
        r=Fraction
    else:
        r=-Fraction
    
    return r,C
    

#Codigo começa aqui

def MKP(website,X,Y): # Make Points
    r = requests.get(website)
    
    Lines=[]
    for line in r.text.split("\n"):
        line=line.split(" ")
        try:
            while True:
                line.remove("")
        except ValueError:
            pass
    
        Lines.append(line)
    
    Lines.pop() 
    
    xi=Lines[0].index(X)
    yi=Lines[0].index(Y)
    
    Lines=Lines[2::]
    
    xs=[]
    ys=[]
    for Line in Lines:
        xs.append(float(Line[xi]))
        ys.append(float(Line[yi]))
        
        
    points=[i for i in zip(xs,ys)]
    
    return xs,ys,points

def Fae(website,X,Y,All=False):
    xs,ys,points = MKP(website,X,Y)
    
    r,C=Cor(points,X,Y,Allpass=All)
    
    se=(C[0])**(1/2)
    
    a=(C[1].split('*'))[0]
    stra=''
    for char in a:
        if char == ' ':
            pass
        else:
            stra+=char
    a=float(stra)
    if not All:
        print(f'r = {r}')
        print(f'se = {se}')
    n=len(points)
    tac=r*((n-2)/(1-r**2))**(1/2)

    if not All:
        print(f't = {tac}')
    
    ndf = len(points)-2
    p = 0.975
    tc = t.ppf(p, ndf)
    
    if not All:
        print (f"two-side confidence limit for p = 0.95: tc = {tc}")
        
    Xn,Yn,NX,NY=C[2]
    Xm=''
    Ym=''
    ForbidenList = ['\\\\','/','"',':','<','>','|','?','*']
    
    
    for char in X:
        if char not in ForbidenList:
            Xm+=char
        else:
            Xm+='�'
    for char in Y:
        if char not in ForbidenList:
            Ym+=char
        else:
            Ym+='�'
            
            
    if abs(tac)>=tc:
        if not All:
            print(f"\nSince |{tac}| > {tc} we can conclude there is a correlationship\n")
            plt.scatter(Xn,Yn)
            plt.grid
            plt.plot(NX,NY,c='tab:red')
            plt.title(f'{Y} as a function of {X}')
            plt.savefig(f'{cwd}/GraphsFolder/{Ym} as a function of {Xm}')
            plt.show()
            plt.clf()
            plt.close()
        else:
            plt.scatter(Xn,Yn)
            plt.grid
            plt.plot(NX,NY,c='tab:red')
            plt.title(f'{Y} as a function of {X}')
            plt.savefig(f'{cwd}/GraphsFolder/{Ym} as a function of {Xm}')
            plt.clf()
            plt.close()
    else:
        if not All:
            print(f"\nSince |{tac}| < {tc} we can conclude there isn't a correlationship\n")
            plt.scatter(Xn,Yn)
            plt.grid
            plt.plot(NX,NY,c='tab:red')
            plt.savefig(f'{cwd}/GraphsFolder/{Ym} as a function of {Xm}')
            plt.show()
            plt.clf()
            plt.close()
        else:
            plt.figure()
            plt.clf()
            plt.close()
            
    xs=np.array(xs,dtype=float)
    xsum=np.sum(xs/len(points))
    xsum2n=((xsum)**2)*len(points)
    xSum2=np.sum(xs**2)
    
    root=(xSum2-xsum2n)**(1/2)
    
    sa=se/root
    deltax=tc*sa
    if not All:
        print(f'\nsa = {sa}')
        print(f"\na = {a}")
        print(f"∆a = {deltax}")
        print(Based(float(a),float(deltax)))
        
    plt.clf()
    plt.close()
    
    
Single=eval(input("Find all correlations ? = "))


r = requests.get('https://trixi.coimbra.lip.pt/courteau/courteau99.dat')

text=r.text.split("\n")
text=text[0].split(" ")
try:
    while True:
        text.remove("")
except ValueError:
    pass

print(f'List = {text}')

if Single:
    c=0
    for X in text:
        for Y in text:
            c+=1
            print(f"{c/(int(len(text))**2)*100:.5f}%",end='\r')
            if X != Y:
                try:
                    Fae('https://trixi.coimbra.lip.pt/courteau/courteau99.dat',X,Y,All=True)
                except:
                    print(f"Error on X = {X} and Y = {Y}")
else:
    X=input("First Variable = ")
    Y=input("Second Variable = ")
    Fae('https://trixi.coimbra.lip.pt/courteau/courteau99.dat',X,Y,All=False)
    

input("Press Enter To Close")