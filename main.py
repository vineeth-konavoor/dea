import random
from matplotlib import pyplot as plt
import numpy as np

def Fitness(L): #Fitness function
    h=0
    for var in L:
        h+=var*var
    return 1/(h+0.01)
def column(A,j): #function to extract jth column from a given matrix A
    A_j=[]
    for i in range(len(A)):
       A_j.append(A[i][j])
    return A_j

def addEpsilon(A,e): #add the value e to every element of the given matrix A
    for i in range(len(A)):
        for j in range(len(A[0])):
            A[i][j]+=e
    return A

error=[]
errors=[]
param=[]
xmin=-20
xmax=20
step=0.01
NL=50
NV=4
LoopsNumber=50
PP=[]                   # Defining required constant values
PP1=0.11

Re=int((xmax-xmin)/4)
Epsilon=0.01

L=[]
L_init=[]
Fit=[]
Alternatives=[]
AF=[]
i=0
while i <= xmax:  # prerequisites
    a = []
    af = []
    for j in range(NV):
        a.append(i)  # Making the alternatives matrix and
        af.append(0)  # Also initiating the Accumulative Fitnesss with 0s
    Alternatives.append(a)
    AF.append(af)
    i += step

for i in range(NL):
    li = []
    for j in range(NV):  # making random locations for initial search
        li.append(random.choice(column(Alternatives, j)))  # creating random locations
    L_init.append(li)
    Fit.append(0)
    L.append(li)
print(L_init[0])
for n in [0.5,0.75,1,1.25,1.5]:
    error=[]
    Fit=[]
    Power=0.2*n
    for h in range(len(L_init)):
        for v in range(len(L_init[0])):
            L[h][v]=L_init[h][v]
    print(L_init[0])
    for i in range(NL):
        Fit.append(0)
    while i <= xmax:  # prerequisites
        for j in range(NV):
            AF[i][j]=0
        i += step
    PP=[]
    for loop in range(1,LoopsNumber): #main Loop

        PPi=PP1+((1-PP1)*((loop**Power)-1)/((LoopsNumber**Power)-1))
        PP.append(PPi)
        for LocationNumber in range(NL):
            Fit[LocationNumber]=Fitness(L[LocationNumber]) #Fit matrix has Fitnesss of all locations
        for i in range(NL): #step 4
            for j in range(NV):
                jthColumnOfAlt=column(Alternatives,j)

                A=jthColumnOfAlt.index(L[i][j])       #finding jth column and finding Lij in that column
                for k in range(-Re,Re):
                    if (A+k)>=0 and (A+k)<len(Alternatives):
                        s=A+k
                        AF[A+k][j]+=(1/Re)*(Re-abs(k))*Fit[i]


        AF=addEpsilon(AF,Epsilon) #step 4 b. adding epsilon


        #step 4 c
        BestLocation=L[Fit.index(max(Fit))]


        for j in range(NV):
            for i in range(len(Alternatives)):
                if Alternatives[i][j]==BestLocation[j]:
                    AF[i][j]=0


        sumAF=0 #step 5
        for i in range(len(AF)):
            for j in range(len(AF[0])):
                sumAF+=AF[i][j]
        P=[]
        for i in range(len(Alternatives)):
            p=[]
            for j in range(NV):
                p.append(AF[i][j]/sumAF)
            P.append(p)


        for j in range(NV): #step 6
            for i in range(len(Alternatives)):
                if Alternatives[i][j]==BestLocation[j]:
                    P[i][j]=PPi
                else:
                    P[i][j] *= (1-PPi)
        # x = []
        # y = []
        # clr = []
        # for pt in L:
        #     x.append(pt[0])
        #     y.append(pt[1])
        #     xalt = column(Alternatives, 0)
        #     yalt = column(Alternatives, 1)
        #     xidx = xalt.index(pt[0])
        #     yidx = yalt.index(pt[1])
        #     xclr = P[xidx][0]
        #     yclr = P[yidx][1]
        #     clr.append(xclr + yclr)
        # plt.xlim((xmin, xmax))
        # plt.ylim((xmin, xmax))
        # #plt.scatter(x, y, c=clr, cmap='Reds')
        # plt.scatter(x, y, c='blue')
        # plt.show()

        #generating next L matrix according to P

        for i in range(NL):
            location=[]
            for j in range(NV):
                temp_probs=column(P,j)
                probs=[]
                s=sum(temp_probs)
                for value in temp_probs:
                    probs.append(value/s)
                alts=column(Alternatives,j)
                val=np.random.choice(alts,p=probs)
                location.append(val)
            L[i]=location

        err=0
        for val in BestLocation:
            err+=(val*val)
        error.append(np.sqrt(err))

        out=str(loop)+" & "+str(np.sqrt(err))+"\\\\ "+"\\hline"
        print(out)
    errors.append(error)
n=0.5
for i in range(len(errors[0])):
    param.append(i)
for error in errors:
    lbl="Power = "+str(n)
    plt.plot(param,error,label=lbl)
    print(error)
    n=n+0.25
plt.ylabel("Error")
plt.xlabel("Number of Loops")
plt.legend()
plt.show()
