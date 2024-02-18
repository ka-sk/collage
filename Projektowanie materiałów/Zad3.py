"""
Dla sytuacji z zad. 2, wyznacz stałą sieci oraz grubość krytyczną hc dla materiału studni w funkcji
składu. Grubość krytyczną wyznacz ze wzoru hc=a1a0/|a1-a0|.
"""
import matplotlib.pyplot as plt
import numpy as np
import functions as funny  # funkcje dołączone w projekcie

# definicja materiałów początkowych
InP = {
    "a": 5.8697,  # 1e-10 m
    "Eg": 1.4236,  # eV
    "VBO": -0.94,  # eV
    "a_v": -0.6,  # eV
    "a_c": -6.0  # eV
       }

InSb = {
    "a": 6.4794,  # 1e-10 m
    "Eg": 0.235,  # eV
    "VBO": 0,  # eV
    "a_v": -0.36,  # eV
    "a_c": -6.94  # eV
       }

GaAs = {
    "a": 5.65325,  # 1e-10 m
    "Eg": 1.519,  # eV
    "VBO": -0.80,  # eV
    "a_v": -1.16,  # eV
    "a_c": -7.17  # eV
       }

# stała sieciowa materiału otoczenia
a_0 = GaAs["a"]

# stworzenie listy dla stężenia
x = np.linspace(0, 1, 100)

# stworzenie listy stałych sieciowych na podstawie stężenia
a = funny.stop(InP["a"], InSb["a"], x)

# stworzenie obrazka nr 1
plt.figure(1, figsize=(6, 10))
# wykres 1 obrazka 1: a(x)
plt.subplot(211)
# tytuł wykresu
plt.title("Wykres zależności stałej sieciowej od stężenia InP")
# wykres
plt.plot(x, a, "b-.")
# opisanie osi
plt.xlabel("Stężenie [a.u.]")
plt.ylabel("Stała sieciowa [*10**-10 m]")


hc = np.empty_like(x)

for i in range(len(a)):
    if a[i] != a_0:
        hc[i] = a[i] * a_0 / (a[i] - a_0)
    else:
        x = np.delete(x, i)
        hc = np.delete(hc, i)

plt.subplot(212)
plt.title("Wykres zależności grubości krytycznej studni od stężenia InP")
plt.plot(x, hc, "r:")
plt.xlabel("Stężenie [a.u.]")
plt.ylabel('Grubość krytyczna [*10**-10 m]')

plt.show()


