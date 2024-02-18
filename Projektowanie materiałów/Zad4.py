"""
Dla jednego z wybranych podłoży, zaproponuj stop czteroskładnikowy dopasowany sieciowo do
podłoża, którym można uzyskać przerwę wbronioną o zadanej długości fali (GaAs-620nm, InP-
1240nm, InAs-1650nm, GaSb-990nm). Zaproponuj stop trójskładnikowy, którym można uzyskać
taką samą przerwę. Dla obu związków narysuj jak zmienia się przerwa wzbroniona w całym
zakresie składów. Dla stopu trójskładnikowego narysuj przypadek z i bez uwzględnienia naprężeń
"""

import functions as funny
import numpy as np
import matplotlib.pyplot as plt

# Podłoże GaSb - 990 nm

lam = 990 * 1e-9  # m
hc = 1.23984198 * 1e-6  # eV*m

# obliczenie przerwy wzbronionej
Energy_gap = hc / lam

print(f"Przerwa energetyczna wynosi {round(Energy_gap, 2)}eV")
print("Dostosowane jest AlGaAsSb")
# dopasowane jest AlGaAsSb

# AlAsSb musi być dopasowany sieciowo do GaSb

GaSb = {
    "a": 6.0959,  # A
    "Eg": 0.812,  # eV
    "VBO": -0.03,  # eV
    "a_v": -0.8,  # eV
    "a_c": -7.5  # eV
}

# AlAs

AlAs = {
    "a": 5.6611,  # A
    "Eg": 3.099,  # eV
    "VBO": -1.33,  # eV
    "a_v": -2.47,  # eV
    "a_c": -5.64  # eV
}

# AlSb

AlSb = {
    "a": 6.1355,  # A
    "Eg": 2.386,  # eV
    "VBO": -0.41,  # eV
    "a_v": -1.4,  # eV
    "a_c": -4.5  # eV
}

conc1 = funny.conc(AlAs["a"], AlSb['a'], GaSb['a'])

AlAsSb = funny.stop(AlAs, AlSb, conc1)
AlAsSb["Eg"] = funny.stop(AlAs["Eg"], AlSb["Eg"], conc1, 0.8)

conc2 = funny.conc(GaSb['Eg'], AlAsSb["Eg"], Energy_gap, 0.47)

print(
    f"Finalny stop wyraża się wzorem: GaSb({round(conc2, 2)})(AlAs({round(conc1, 2)})Sb({round(1 - conc1, 2)}))({round(1 - conc2, 2)})")

##########################################################################
# usuwanie zmiennych
del AlAsSb
del conc2
del conc1
del hc
del lam

##########################################################################
# teraz obliczamy koncentracje dla stopu czteroskładnikowego
# liczba punktów
P_NUMBER = 100

# koncentracja x (czteroskładnikowy)
x = np.linspace(0, 1, P_NUMBER)

# koncentracja y (trójskładnikowego)
y = np.linspace(0, 1, P_NUMBER)

# stworzenie mieszaniny AlAsSb dla każdego możliwego y
AlAsSb = {"a": funny.stop(AlAs["a"], AlSb["a"], y),
          "Eg": funny.stop(AlAs["Eg"], AlSb["Eg"], y, 0.8),
          'a_v': funny.stop(AlAs["a_v"], AlSb["a_v"], y),
          'a_c': funny.stop(AlAs["a_c"], AlSb["a_c"], y)}

# stworzenie macierzy dwuwymiarowej, z wartościami a oraz Eg dla stopu w całym zakresie składów
AlGaAsSb = {"a": np.empty((P_NUMBER, P_NUMBER)),
            "Eg": np.empty((P_NUMBER, P_NUMBER)),
            "Eg_n": np.empty((P_NUMBER, P_NUMBER)),
            "a_v": np.empty((P_NUMBER, P_NUMBER)),
            "a_c": np.empty((P_NUMBER, P_NUMBER))}

AlGaAsSb_t = np.empty((P_NUMBER, P_NUMBER))

# stworzenie macierzy dwuwymiarowej, z wartościami naprężeń dla stopu w całym zakresie składów
epsilon = np.empty((P_NUMBER, P_NUMBER))

# obliczanie Eg
for i in range(P_NUMBER):
    AlGaAsSb["a"][i, :] = funny.stop(GaSb['a'], AlAsSb["a"], x[i])
    AlGaAsSb["a_c"][i, :] = funny.stop(GaSb['a_c'], AlAsSb["a_c"], x[i])
    AlGaAsSb["a_v"][i, :] = funny.stop(GaSb['a_v'], AlAsSb["a_v"], x[i])

    AlGaAsSb["Eg"][i, :] = funny.stop(GaSb['Eg'], AlAsSb["Eg"], x[i], 0.48)
    epsilon[i, :] = funny.epsilon(GaSb["a"], AlGaAsSb["a"][i, :])

    AlGaAsSb["Eg_n"][i, :] = funny.stop(GaSb['Eg'], AlAsSb["Eg"], x[i], 0.48) + epsilon[i, :] * (
                AlGaAsSb["a_v"][i, :] + AlGaAsSb["a_c"][i, :])

##############################################################################
# CZY TO JEST DOBRZE
##############################################################################
plt.figure(1, [15, 7])
# colour grading
plt.subplot(121)
plt.contourf(x, y, AlGaAsSb["Eg"], levels=30, cmap='plasma')
# dodanie color bar
plt.colorbar(label="Eg [eV]")
# opis osi
plt.xlabel("x [a.u.]")
plt.ylabel("y [a.u.]")
plt.title("zmiana Eg od składu dla AlGaAsSb bez uwzględnienia naprężeń")

# rysowanie wykresu z naprężeniami
plt.subplot(122)
plt.contourf(x, y, AlGaAsSb["Eg_n"], levels=30, cmap='plasma')
# dodanie color bar
plt.colorbar(label="Eg [eV]")
# opis osi
plt.xlabel("x [a.u.]")
plt.ylabel("y [a.u.]")
plt.title("zmiana Eg od składu dla AlGaAsSb z uwzględnieniem naprężeń")

# rysowanie naprężeń
plt.figure(2)
# dokładnie to samo co powyżej
plt.contourf(x, y, epsilon, levels=30, cmap='plasma')
plt.colorbar(label="epsilon")
plt.xlabel("x [a.u.]")
plt.ylabel("y [a.u.]")
plt.title("Wykres naprężeń od składu dla AlGaAsSb")
# plt.vlines(0, 0, 1,  linestyles='dashed')

# stop trójskładnikowy
# wybrany stop to AlInAs

InAs = {
    "a": 6.0583,  # A
    "Eg": 0.417,  # eV
    "VBO": 20.59,  # eV
    "a_v": -1.00,  # eV
    "a_c": -5.08  # eV
       }

# znalezienie stopu trójskładnikowego
conc = funny.conc(AlAs['Eg'], InAs['Eg'], Energy_gap, 0.70)
print(f"Stop trójskładnikowy z dopasowaną przerwą energetyczną to Al({round(conc, 2)})In({round(1-conc, 2)})As")

x = np.linspace(0, 1, 100)

AlInAs = funny.stop(AlAs, InAs, x)

AlInAs['Eg'] = funny.stop(AlAs['Eg'], InAs['Eg'], x, 0.70)

epsilon = funny.epsilon(GaSb['a'], AlInAs['a'])

AlInAs["Eg_n"] = AlInAs['Eg'] + epsilon * (AlInAs['a_v'] + AlInAs['a_c'])

plt.figure(3)
plt.plot(x * 100, AlInAs['Eg'], 'b', label='bez naprężeń')
plt.plot(x * 100, AlInAs['Eg_n'], 'r', label ='z naprężeniami')
plt.hlines(GaSb['Eg'], 0, 100, colors='green', linestyle='dashed', label = 'Eg podłoża')
plt.title("Zmiana przerwy energetycznej AlInAs na podłożu GaSb")
plt.xlabel('x [%]')
plt.ylabel('energy gap [eV]')
plt.legend()

plt.show()


