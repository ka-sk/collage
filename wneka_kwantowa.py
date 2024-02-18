import numpy as np
import math as math
import matplotlib.pyplot as plt

a=266*10**(-10)
#m
V0=4.28535*10**(-20)
#J
m0=9.10938291*10**(-31)
#kg
mw=0.067*m0
#kg 
mb=0.094*m0
#kg
h=1.054*10**-34
#J*s
kpmax=3*np.pi/a

kplist=np.linspace(0,kpmax,1000)
Elist=np.linspace(0,V0,100000)
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

"""
plt.figure(1)
plt.plot(Elist,vallist1)
plt.axis([0,5*10**-20,-(10**3),10**3])
plt.figure(2)
plt.plot(Elist,vallist2)
plt.axis([0,5*10**-20,-(10**18),10**18])
plt.figure(1)
plt.plot(Elist,tanlist1)
"""
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
print("tanlist",t1)
print (ilist1)
x1=Elist[ilist1]
x1E=Elist[ilist1]/(1.602*10**-19)
print (ilist2)
x2=Elist[ilist2]
x2E=Elist[ilist2]/(1.602*10**-19)
print("x1E",x1)
print("x2E",x2)

x1new=[]
x2new=[]
for i in range(len(x1)):
    if x1[i] not in t1:
        x1new.append(x1[i])
print(x1new)

for i in range(len(x2)):
    if x2[i] not in t2:
        x2new.append(x2[i])
print(x2new)

zeroplaces=x1new+x2new
zeroplaces=sorted(zeroplaces)
print (zeroplaces)

###################################################################################

plt.figure()

for i in range(len(zeroplaces)):
    E=(h**2*kplist**2/2/mw+zeroplaces[i])/1.602/10**(-22)
    plt.plot(kplist,E,label=f"E{i}={round(zeroplaces[i]/1.602/10**(-22),2)} meV")
    plt.axhline(zeroplaces[i]/1.602/10**(-22),linestyle=":")
    plt.ylabel("E[meV]")
    plt.xlabel("kp[1/m]")
plt.legend(fontsize=8)
plt.show()















 