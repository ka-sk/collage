"""
Narysuj profil energetyczny studni kwantowej, gdzie materiałem studni jest stop z
zad. 1, a materiałem bariery jest GaAs. Narysuj przypadek dla x=0.25 oraz x=0.75.
Pokaż jaki jest profil z i bez uwzględnienia naprężeń (załóż izotropowe
ściskanie/rozciąganie materiału studni). Jaki jest to typ studni? Czy istnieje skład dla
którego materiał studni jest dopasowany sieciowo do GaAs?
"""
import matplotlib.pyplot as plt
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

# definicja bowingu dla stopu InPSb
bowing_Eg = 1.9  # eV

# ------------------------
# STĘŻENIE 0.25
# ------------------------

# definicja stopu dla stężenia x = 0.25
InPSb_25 = funny.stop(InP, InSb, 0.25)

# uwzględnienie bowingu w przerwie energetycznej
InPSb_25["Eg"] = funny.stop(InP["Eg"], InSb['Eg'], 0.25, bowing_Eg)

# stworzenie pierwszego wykresu
fig1 = plt.figure(1, figsize=(10, 6))

# stworzenie zmiennej pomocniczej zawierającej odpowiednie punkty wykresu
wykres = funny.quantum_well(InPSb_25, GaAs)

# pierwszy wykres pierwszego obrazka
plt.subplot(121)
# nakreślenie pasm energetycznych bez uwzględnienia naprężeń
# pasmo walencyjne (czerwone ciągłe)
plt.plot(wykres[0], wykres[1], 'r', label='VB bez naprężeń')
# pasmo przewodnictwa (niebieskie ciągłe)
plt.plot(wykres[0], wykres[2], 'b', label='CB bez naprężeń')
# opisanie osi y
plt.ylabel('Energia [eV]')
# tytuł
plt.title('Schemat studni kwantowej dla InPSb (x = 25)')

# uwzględnienie naprężeń

axis = [0, 3, -1.6, 2.5]

# obliczenie odkształcenia
eps = funny.epsilon(GaAs["a"], InPSb_25["a"])

# podmienienie wartości z naprężeniami w zmiennej pomocniczej
wykres = funny.quantum_well(InPSb_25, GaAs, eps)
# nakreślenie pasm energetycznych bez uwzględnienia naprężeń
# pasmo walencyjne (czerwone przerywane)
plt.plot(wykres[0], wykres[1], 'r--', label='VB z naprężeniami')
# pasmo przewodnictwa (niebieskie przerywane)
plt.plot(wykres[0], wykres[2], 'b--', label='CB z naprężeniami')
# dopasowanie osi x i y by były takie same dla obu stężeń
plt.axis(axis)

# ------------------------
# STĘŻENIE 0.75
# ------------------------

# definicja stopu dla stężenia x = 0.75
InPSb_75 = funny.stop(InP, InSb, 0.75)

# uwzględnienie bowingu w przerwie energetycznej
InPSb_75["Eg"] = funny.stop(InP["Eg"], InSb['Eg'], 0.75, bowing_Eg)

# drugi wykres pierwszego obrazka
plt.subplot(122)
# ponownie zmienna pomocnicza
wykres = funny.quantum_well(InPSb_75, GaAs)
# nakreślenie pasm energetycznych bez uwzględnienia naprężeń
# pasmo walencyjne (czerwone ciągłe)
plt.plot(wykres[0], wykres[1], 'r', label='VB bez naprężeń')
# pasmo przewodnictwa (niebieskie ciągłe)
plt.plot(wykres[0], wykres[2], 'b', label='CB bez naprężeń')
# tytuł
plt.title('dla InPSb (x = 75)')

# uwzględnienie naprężeń

# obliczenie odkształcenia
eps = funny.epsilon(GaAs["a"], InPSb_75["a"])
# podmienienie wartości z naprężeniami w zmiennej pomocniczej
wykres = funny.quantum_well(InPSb_75, GaAs, eps)
# nakreślenie pasm energetycznych bez uwzględnienia naprężeń
# pasmo walencyjne (czerwone przerywane)
plt.plot(wykres[0], wykres[1], 'r--', label='VB z naprężeniami')
# pasmo przewodnictwa (niebieskie przerywane)
plt.plot(wykres[0], wykres[2], 'b--', label='CB z naprężeniami')
# dopasowanie osi x i y by były takie same dla obu stężeń
plt.axis(axis)
# wyświetlenie legendy w prawym dolnym rogu
plt.legend(loc='upper right')

# wyświetlenie wykresów
plt.show()
