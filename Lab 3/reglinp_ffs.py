import matplotlib.pyplot as plt
from math import sqrt
from numpy import polyfit

######################################################################################################################


def niepewnosc_napiecia(U):
    return (0.0012 * U + 0.01)/sqrt(3)


def niepewnosc_natezenia(I, Iz):
    return (0.04 * I + 0.02 * Iz)/sqrt(3)

######################################################################################################################


def read_file(name):
    file = open(r'Dane_pomiarowe/' + name + '_f.txt', 'r')

    x = []
    y = []
    x_z = []
    for line in file.readlines():
        line = line.rstrip("\n")
        line = line.split("\t")
        x.append(float(line[0]))
        y.append(float(line[1]))
        x_z.append(float(line[3]))

    file.close()

    return x, y, x_z


def safe_file(x: list, x_err: list, y: list, y_err: list, name: str):
    file = open(r'Wyniki_obliczeń/' + name + '_linfit.txt', 'w')

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

######################################################################################################################


file_names = ["czerwona", "niebieska", "zielona", "żółta", 'biala']

colors = ['#f94144', '#43aa8b', '#90be6d', '#f9c74f', '#979dac']

add_colors = ['#FDB0B1', '#B6E2D5', '#BFD9AB', '#FBDF9D', '#BBBFC9']

font_color = ['#8a0507', '#235848', '#44632c', '#8A6205', '#2D3139']

titles = ["czerwonej", 'niebieskiej', 'zielonej', 'żółtej', 'białej']

wyniki_pomiarow = {}

#for i in range(1):  # do testów
for i in range(len(file_names)):

    #odczytanie danych pomiarowych z pliku
    I, U, I_z = read_file(file_names[i])

    # Niepewności
    I_e = [niepewnosc_natezenia(I[j], I_z[j]) for j in range(len(I))]
    U_e = [niepewnosc_napiecia(j) for j in U]

    # zaokrąglenia danych pomairowych
    I, I_e = zaokraglenie(I, I_e)
    U, U_e = zaokraglenie(U, U_e)

    a, b = polyfit(U, I, 1)
    print(f'{file_names[i]}: a={a}, b={b}')
    linfit = [a*j+b for j in U]

    #Wykresy
    plt.figure(i)
    plt.errorbar(U, I, I_e, U_e, '.', c=colors[i], label='Wyniki pomiarów')
    plt.plot(U, linfit, '--', c=add_colors[i], label='Przybliżenie liniowe')
    plt.title("Zależność prądu fotodiody " + titles[i] + " w funkcji prądu zasilającego LED")
    plt.ylabel("fotoprąd [nA]")
    plt.xlabel("Prąd zasilania [mV]")
    plt.legend(labelcolor=font_color[i])

    #zapisanie do pliku
    safe_file(U, U_e, I, I_e, file_names[i])


plt.show()
