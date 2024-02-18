"""
Dla wybranego stopu trójskładnikowego AxB1-x narysuj jak zmienia się przerwa
energetyczna oraz stała sieci w funkcji x, (dla przerwy energetycznej uwzględnij
bowing). Dla x=0.5 narysuj jak zmienia się przerwa energetyczna w funkcji
temperatury w zakresie 0 do 300 K.
"""

import matplotlib.pyplot as plt
import numpy as np
import functions as funny  # funkcje dołączone w projekcie


# definicja materiałów początkowych
InP = {
    "a": 5.8697,  # 1e-10 m
    "Eg": 1.4236,  # eV
    "alpha": 0.363 * 1e-3,  # eV/K
    "beta": 162,  # K
       }

InSb = {
    "a": 6.4794,  # 1e-10 m
    "Eg": 0.235,  # eV
    "alpha": 0.32 * 1e-3,  # eV/K
    "beta": 170,  # K
       }

# definicja bowingu dla stopu InPSb
bowing_Eg = 1.9  # eV

# definicja stężenia stopu
x = np.linspace(0, 1, 100)

# obliczenie stałej sieciowej (bowing = 0)
a = funny.stop(InP['a'], InSb['a'], x)

# obliczenie przerwy energetycznej z uwzględnieniem bowingu
Eg = funny.stop(InP['Eg'], InSb['Eg'], x, bowing_Eg)

# Stworzenie obrazka 6*9 cali
fig1 = plt.figure(1, figsize=(6, 10))
# obrazek z dwoma wykresami w pionie
plt.subplot(211)
plt.title("Zmiana parametrów InPSb w zalezności od koncentracji InP")
# wykres a(x)
plt.plot(x * 100, a, "m*")
plt.ylabel("Stała sieciowa [1e-10 m]")

# stworzenie drugiego wykresu pierwszego obrazka
plt.subplot(212)
# wykres Eg(x)
plt.plot(x * 100, Eg, "c*")
plt.ylabel("Przerwa Energetyczna [eV]")
plt.xlabel("Koncentracja [%]")



# zwolnienie nieużywanej pamięci
del x
del a

# definicja stopu dla stężenia x = 0.5
InPSb = funny.stop(InP, InSb, 0.5)
# uwzględnienie bowingu w stopie o stężeniu x = 0.5
InPSb["Eg"] = funny.stop(InP["Eg"], InSb['Eg'], 0.5, bowing_Eg)

# definicja temperatury
T = np.linspace(0, 300, 100)
Eg = funny.Eg_T(T, InPSb["Eg"], InPSb["alpha"], InPSb["beta"])

# wyświetlenie drugiej części zadania
fig2 = plt.figure(2, figsize=(7, 5))
plt.plot(T, Eg, 'bX')
plt.title("Zmiana przerwy energetycznej w InPSb w zależności od temperatury (x = 0.5)")
plt.ylabel("Przerwa Energetyczna [eV]")
plt.xlabel("Temperatura [K]")

plt.show()





