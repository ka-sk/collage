import matplotlib.pyplot as plt
from math import sqrt

h = 6.62607015 * 10**(-34)  # J*s
c = 299792458  # m/s

######################################################################################################################


def niepewnosc_napiecia(U, del_U):
    return (0.0012 * U + del_U)/sqrt(3)


def niepewnosc_natezenia(I, Iz):
    return (0.04 * I + 0.02 * Iz)/sqrt(3)


def niepewnosc_lambdy():
    return 5/sqrt(3) #nm


def niepewnosc_energii(lamb, u_lamb):
    return h*c*u_lamb/lamb**2


def energia(lamb):
    return h*c/lamb


######################################################################################################################


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


def safe_file(x: list, x_err: list, y: list, y_err: list, name: str, additional:dict):
    file = open(r'Wyniki_obliczeń/' + name + '.txt', 'w')

    [file.writelines(str(x[nr]) + "\t" + str(x_err[nr]) + "\t" + str(y[nr]) + "\t" + str(y_err[nr]) + "\n") for nr in range(len(x))]

    file.writelines("\n\nDodatkowe Parametry:\n\n")

    [file.writelines(str(key) + ': ' + str(additional[key]) + '\n') for key in additional.keys()]

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


def zaokr_s(d: dict):
    data = []
    error = []
    for key in d.keys():
        if 'error' not in key:
            d[key], d[key + '_error'] = zaokraglenie(d[key], d[key + '_error'])
    return d


def szer_pol(lamb, intensity):
    indexes = []
    for i in range(len(intensity)):
        if intensity[i] >= 50:
            indexes.append(i)
    return [lamb[indexes[0]], lamb[indexes[-1]]]

######################################################################################################################


file_names = ["czerwona", "niebieska", "zielona", "żółta"]

colors = ['#f94144', '#43aa8b', '#90be6d', '#f9c74f']

add_colors = ['#FDB0B1', '#B6E2D5', '#BFD9AB', '#FBDF9D']

font_color = ['#8a0507', '#235848', '#44632c', '#8A6205']

titles = ["czerwonej", 'niebieskiej', 'zielonej', 'żółtej']

wyniki_pomiarow = {}

#for i in range(1):  # do testów
for i in range(len(file_names)):

    #odczytanie danych pomiarowych z pliku
    lamb, intensity = read_file(file_names[i])

    #obliczenie niepewności ze wzorów
    lamb_error = [niepewnosc_lambdy()] * len(lamb)
    intensity_error = [niepewnosc_natezenia(i, 100) for i in intensity]

    # zaokrąglenia danych pomairowych
    lamb, lamb_error = zaokraglenie(lamb, lamb_error)
    intensity, intensity_error = zaokraglenie(intensity, intensity_error)

    #wyznaczenie lamb max
    wyniki_pomiarow["lamb_max"] = lamb[intensity.index(max(intensity))]
    wyniki_pomiarow['lamb_max_error'] = niepewnosc_lambdy()

    # wyzanczenie Eg i niepewnosci
    wyniki_pomiarow['Eg[J]'] = energia(wyniki_pomiarow['lamb_max']*10**(-9))
    wyniki_pomiarow['Eg[J]_error'] = niepewnosc_energii(wyniki_pomiarow['lamb_max']*10**(-9), wyniki_pomiarow['lamb_max_error']*10**(-9))

    # wyznaczenie szerokości połówkowej
    wyniki_pomiarow['szer_pol1'], wyniki_pomiarow['szer_pol2'] = szer_pol(lamb, intensity)
    wyniki_pomiarow['szer_pol1_error'] = 2 * niepewnosc_lambdy()
    wyniki_pomiarow['szer_pol2_error'] = 2 * niepewnosc_lambdy()

    # zaokraglenie wyników
    zaokr_s(wyniki_pomiarow)

    #Wykresy
    plt.figure(i)
    plt.errorbar(lamb, intensity, intensity_error, lamb_error, '.', c=colors[i], label='Wyniki pomiarów')
    plt.vlines(wyniki_pomiarow['lamb_max'], 0, 100, colors=add_colors[i], linestyles='dashed', label='λ max')
    plt.hlines(50, wyniki_pomiarow['szer_pol1'], wyniki_pomiarow['szer_pol2'], colors=add_colors[i], linestyles='dashdot', label='Δλ')
    plt.title("Wykres intensywności diody " + titles[i] + ' w zależności od długości fali')
    plt.xlabel("Długość fali [nm]")
    plt.ylabel("Względna intensywność [%]")
    plt.legend(labelcolor=font_color[i])

    #zapisanie do pliku
    safe_file(lamb, lamb_error, intensity, intensity_error, file_names[i], wyniki_pomiarow)


plt.show()
