import numpy as np
import matplotlib.pyplot as plt

a=666*10**(-10)
#m
V0=1.602*10**-19
#J
m0=9.10938291*10**(-31)
#kg
mw=0.1*m0
#kg 
mb=0.1*m0
#kg
h=1.054*10**-34
#J*s
kpmax=10*np.pi/a
mb=mw
def find_zeroplaces(a,V0,mw,mb):
    kplist=np.linspace(0,kpmax,100)
    Elist=np.linspace(0,2*V0,1000)
    vallist1=[]
    vallist2=[]
    kwlist=[]
    tanlist1=[]
    tanlist2=[]
    
    for i in range(len(Elist)):
        kw=(2*mw/(h**2)*Elist[i])**(0.5)
        kwlist.append(kw)
        kb=((-2)*mb/(h**2)*(Elist[i]-V0))**0.5
        tanlist1.append(np.tan(kw*a/2))
        vallist1.append(kb/mb-kw/mw*tanlist1[i])
        tanlist2.append(1/np.tan(kw*a/2))
        vallist2.append(kb/mb+kw/mw*tanlist2[i])
    '''
    plt.figure(1)
    plt.plot(Elist,vallist1)
    plt.axis([0,5*10**-20,-(10**3),10**3])
    plt.figure(2)
    plt.plot(Elist,vallist2)
    plt.axis([0,5*10**-20,-(10**18),10**18])
    plt.figure(1)
    plt.plot(Elist,tanlist1)
    '''
    ilist1=[]
    ilist2=[]
    tanilist1=[]
    tanilist2=[]
    counter=0
    for i in range (len(Elist)-1):
        if vallist1[i]*vallist1[i+1]<0:
            ilist1.append(i)
        if tanlist1[i]*tanlist1[i+1]<0:
            tanilist1.append(i)
        if tanlist2[i]*tanlist2[i+1]<0:
            tanilist2.append(i)
        if vallist2[i]*vallist2[i+1]<0:
            ilist2.append(i)
        else:
            counter+=1
    t1=Elist[tanilist1]
    t2=Elist[tanilist2]
    
    x1=Elist[ilist1]
    x1E=Elist[ilist1]/(1.602*10**-19)
    
    x2=Elist[ilist2]
    x2E=Elist[ilist2]/(1.602*10**-19)
    
    x1new=[]
    x2new=[]
    
    for i in range(len(x1)):
        if x1[i] not in t1:
            x1new.append(x1[i])
    
    for i in range(len(x2)):
        if x2[i] not in t2:
            x2new.append(x2[i])
    
    zeroplaces=x1new+x2new
    zeroplaces=sorted(zeroplaces)
    return(zeroplaces)

alist=np.linspace(1*10**-10,200*10**-10,50)
mlist=np.linspace(0*m0,0.2*m0,50)
resultsa=[]
resultsm=[]
xlista=[]
xlistm=[]
for i in alist:
    reslista=find_zeroplaces(i,V0,mw,mw)
    for j in range(len(reslista)):
        resultsa.append(reslista[j])
        xlista.append(i)
  
#plt.figure(1)
#plt.scatter(xlista,resultsa,s=3)
    
for i in mlist:
    reslistm=find_zeroplaces(150*10**-10,V0,i,i)
    for j in range(len(reslistm)):
        resultsm.append(reslistm[j]/1.602*10**22)
        xlistm.append(i/m0)    

#plt.figure(5)
#plt.scatter(xlistm,resultsm,s=3)
    
    
''''''''''''''
awell=90*10**-10
Vwell=1.602*10**-19
mwell=0.067*m0
    
    
rlist=np.linspace(-awell,awell,10000)
well=[]
for i in rlist:
    if abs(i)>awell/2:
        well.append(Vwell)
    else:
        well.append(0)
plt.figure()
plt.plot(rlist,well)


A=find_zeroplaces(awell,Vwell,mwell,mwell)
res=[[],[],[],[],[]]
wave=[[],[],[],[],[]]
for i in range(len(A)):
    for j in range(len(rlist)):
        res[i].append(A[i])


for i in range(len(A)):
    plt.plot(rlist,res[i],'--')
    
comp=0+1j
kbl=[]
kwl=[]
A1=[10**-18,10**-17/2,-10**-18,-10**-18/1.5]
A2=[-10**-18,-10**-17/2,10**-18,10**-18/1.5]
S1=[10**-20,10**-20/2.5,10**-20,10**-20]
'''
for i in range(len(A)):
    kwl.append(((2*mw/(h**2)*A[i])**(0.5))/10**9/6)
    kbl.append((((-2)*mb/(h**2)*(A[i]-V0))**0.5)/10**9/6)
    S1.append(10**-11*((kbl[i]/np.e**kbl[i]*awell)*(1-A1[i]**2*(2*awell+(np.e**(comp*kwl[i]*awell)/(comp*kwl[i]))-np.e**(-comp*kwl[i]*awell)/comp*kwl[i]))))
    print((kbl[i],np.e**kbl[i]*awell))
    print(np.e**kbl[i])
'''

for i in range(len(A)):
    for k in range(len(rlist)):
        kw=(2*mw/(h**2)*A[i])**(0.5)
        kb=((-2)*mb/(h**2)*(A[i]-V0))**0.5
        if abs(rlist[k])<awell/2:
            wave[i].append(S1[i]*(np.e**(comp*rlist[k]*kw)+np.e**(-rlist[k]*kw*comp))+A[i])
            #print("stud")
        elif rlist[k]>awell/2:
            wave[i].append((-np.e**(-rlist[k]*kb))*A1[i]+A[i])
            #print("rbar")
        elif rlist[k]<-awell/2:
            wave[i].append((np.e**(rlist[k]*kb))*A2[i]+A[i])
            #print("lbar")
    #print(A[i])
    
for i in range(len(A)):
    plt.plot(rlist,wave[i])

plt.show()
            





































