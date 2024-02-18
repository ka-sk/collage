import matplotlib.pyplot as plt
from math import sqrt

h = 6.62607015 * 10**(-34)  # J*s
c = 299792458  # m/s

##############################################################


def niepewnosc_natezenia(I, Iz):
    return (0.04 * I + 0.02 * Iz)/sqrt(3)


def niepewnosc_lambdy():
    return 5/sqrt(3)  # nm

##############################################################


def read_file(name):
    file = open(r'Dane_pomiarowe/' + name + '.txt', 'r')

    x = []
    y = []
    for line in file.readlines():
        line = line.rstrip("\n")
        line = line.split("\t")
        x.append(float(line[0]))
        y.append(float(line[1]))

    file.close()

    return x, y


def safe_file(x: list, x_err: list, y: list, y_err: list, name: str):
    file = open(r'Wyniki_obliczeń/' + name + '.txt', 'w')

    [file.writelines(str(x[nr]) + "\t" + str(x_err[nr]) + "\t" + str(y[nr]) + "\t" + str(y_err[nr]) + "\n") for nr in range(len(x))]

    file.writelines("\n\nDodatkowe Parametry:\n\n")

    file.close()


def zaokraglenie(x: list, x_err: list):
    if type(x) == list:

        for i in range(len(x)):
            xe = x_err[i]
            xx = x[i]
            multiplier = 1

            while 100 > int(xe) < 10:
                xe *= 10
                xx *= 10
                multiplier *= 0.1

            while int(xe) > 100:
                xe *= 0.1
                xx *= 0.1
                multiplier *= 10
            x_err[i] = float(int(xe) * multiplier)
            x[i] = float(int(xx) * multiplier)

    elif type(x) == float or type(x) == int:
        xe = x_err
        xx = x
        multiplier = 1

        while 100 > int(xe) < 10:
            xe *= 10
            xx *= 10
            multiplier *= 0.1

        while int(xe) > 100:
            xe *= 0.1
            xx *= 0.1
            multiplier *= 10

        x_err = float(int(xe) * multiplier)
        x = float(int(xx) * multiplier)

    return x, x_err

#####################################################


#odczytanie danych pomiarowych z pliku
lamb, intensity = read_file('biala')

#obliczenie niepewności ze wzorów
lamb_error = [niepewnosc_lambdy()] * len(lamb)
intensity_error = [niepewnosc_natezenia(i, 100) for i in intensity]

# zaokrąglenia danych pomairowych
lamb, lamb_error = zaokraglenie(lamb, lamb_error)
intensity, intensity_error = zaokraglenie(intensity, intensity_error)

#Wykresy
plt.figure()
plt.errorbar(lamb, intensity, intensity_error, lamb_error, '.', c='#979dac', label='Wyniki pomiarów')
plt.title("Wykres intensywności diody białej w zależności od długości fali")
plt.xlabel("Długość fali [nm]")
plt.ylabel("Względna intensywność [%]")
plt.legend()

#zapisanie do pliku
safe_file(lamb, lamb_error, intensity, intensity_error, 'biała')

plt.show()