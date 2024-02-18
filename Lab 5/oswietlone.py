from math import sqrt, log,exp
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import curve_fit
import numpy as np

h = 4.13567E-15  # eV * s
c = 299792458  # m / s


#####################################################################################################################
def niepewnosc_U(U):
    return (0.0005 * U + 0.003) / sqrt(3)


def niepewnosc_I(I):
    return (0.005 * I + 0.000003) / sqrt(3)


def niepewnosc_Vbi(a, b, del_a, del_b):
    return sqrt(((del_a * b / a ** 2) ** 2) + (del_b / a) ** 2)


def V_bi(a, b):
    return -b / a


def Eg(lam):
    return h * c / lam


def V_oc(a, b):
    return exp(-b/a)


def niepewnosc_V_oc(a, b, a_err, b_err):
    return sqrt( (-exp(-b/a) * b_err / a)**2 + (b * exp(-b/a) * a_err / (a**2))**2)


######################################################################################################################

def log_fit(x, a, b):
    return [a*log(i) + b for i in x] if type(x) != float and type(x) != int else a*log(x) + b


def read_file(name):
    file = open(name, 'r')

    x = []
    y = []
    for line in file.readlines():
        line = line.rstrip("\n")

        line = line.replace('+', '')
        line = line.replace(',', '.')

        line = line.split("\t")

        x.append(float(line[0]))
        y.append(float(line[1]))

    file.close()

    return x, y


def safe_file(x: list, x_err: list, y: list, y_err: list, name: str, additional: dict):
    file = open(r'Wyniki_obliczeń/Dioda krzemowa/' + name + '.txt', 'w')

    [file.writelines(str(x[nr]) + "\t" + str(x_err[nr]) + "\t" + str(y[nr]) + "\t" + str(y_err[nr]) + "\n") for nr in
     range(len(x))]

    file.writelines("\n\nDodatkowe Parametry:\n\n")

    [file.writelines(str(key) + ':\t' + str(additional[key]) + '\n') for key in additional.keys()]

    file.close()


def zaokraglenie(x: list, x_err: list):
    if type(x) == float or type(x) == int:
        xe = x_err
        xx = x
        multiplier = 1

        if xe >= 100:
            while not 100.0 > xe >= 10.0:
                xe *= 0.1
                xx *= 0.1
                multiplier *= 10
            pass
        elif xe < 10:
            while not 100 > xe >= 10:
                xe *= 10
                xx *= 10
                multiplier *= 10
            pass
        else:
            pass
        x_err = float(int(xe) * multiplier)
        x = float(int(xx) * multiplier)

    elif type(x) == list:
        for i in range(len(x)):
            xe = x_err[i]
            xx = x[i]
            multiplier = 1

            if xe >= 100:
                while not 100.0 > xe >= 10.0:
                    xe *= 0.1
                    xx *= 0.1
                    multiplier *= 10
                pass
            elif xe < 10:
                while not 100 > xe >= 10:
                    xe *= 10
                    xx *= 10
                    multiplier *= 0.1
                pass
            else:
                pass

            x_err[i] = float(int(xe) * multiplier)
            x[i] = float(int(xx) * multiplier)

    return x, x_err


def zaokr_s(d: dict):
    for key in d.keys():
        if 'error' in key:
            d[key[:-6]], d[key] = zaokraglenie(d[key[:-6]], d[key])  # WHAT THE FUCK IS WRONG HERE
    return d

#######################################################################################################################


FILE_NAMES = [ '4', '8', '12', '16', '20', '24', '28', '32', '36', '40']
FIGURE_NR = 2
CURRENTS = [4.0, 8.02, 12.01, 16.01, 20.01, 24.00, 28.00, 31.99, 36.01, 40.15]

wyniki = {}

CURRENTS_ERROR = [niepewnosc_I(i) for i in CURRENTS]

I_sc_list = []
I_sc_e = []
V_oc_list = []
V_oc_e = []

CURRENTS, CURRENTS_ERROR = zaokraglenie(CURRENTS, CURRENTS_ERROR)

COLOURS = ["#435373","#515575","#6d597a","#915f78","#b56576","#cd6873","#e56b6f","#e88c7d","#E99C84","#eaac8b"]

DARK = ["#1e2533","#3b3e54","#4a3c53","#634052","#8a4252","#a83845","#da2f35","#da462f","#dd6540","#dc7841"]

LIGHT = ["#7285ac","#878bab","#9c89a9","#b690a3","#d19fa9","#e6b3b8","#f3babc","#f3c1ba","#f0b9a8","#f0c1a8"]

for index in range(len(FILE_NAMES)):
    U, I = read_file('Better/dioda krzemowa/' + FILE_NAMES[index] + '.txt')

    # sprowadzenie jednostek do SI podstawowych
    U = [i * 10 ** (-3) for i in U]  # V
    I = [i * 10 ** (-3) for i in I]  # A

    # obliczenie niepewności ze wzoru
    I_error = [niepewnosc_I(i) for i in I]  # A
    U_error = [niepewnosc_U(i) for i in U]  # V

    # wycinek do reglinpa
    temp = 0
    U_lin = []
    I_lin = []
    I_lin_e = []
    U_lin_e = []
    while U[temp] < 0.03:
        U_lin.append(U[temp])
        I_lin.append(I[temp])
        I_lin_e.append(I_error[temp])
        U_lin_e.append(U_error[temp])
        temp += 1

    # regresja liniowa
    lin = linregress(U_lin, I_lin)

    a = lin.slope
    b = lin.intercept
    a_err = lin.stderr
    b_err = lin.intercept_stderr

    #zapisanie wyników dotychczasowych
    wyniki['a_lin\t[A/V]'] = a
    wyniki['a_lin_error\t[A/V]'] = a_err
    wyniki['b_lin\t[A]'] = b
    wyniki['b_lin_error\t[A]'] = b_err

    wyniki['I_sc\t[A]'] = b
    wyniki["I_sc_error\t[A]"] = b_err

    I_sc_list.append(b)
    I_sc_e.append(b_err)

    # wykres
    plt.figure(1)
    plt.errorbar(U, I, I_error, U_error, ".", markersize=3, c=COLOURS[index], label='%.0f'%CURRENTS[index] + 'mA')
    plt.plot(0, b, 'x', c=DARK[index], markersize=10)
    plt.axhline(0, c='#d6ccc2', lw=0.1)
    plt.axvline(0, c='#d6ccc2', lw=0.1)
    plt.xlabel('U [V]')
    plt.ylabel('I [A]')
    plt.title('Charakterystyka prądowo-napięciowa fotodiody oświetlanej dla różnych prądów zasilania oświetlenia')
    plt.plot([U_lin[0], U_lin[-1]], [U_lin[0]*a + b, U_lin[-1]*a+b], c=LIGHT[index])
    plt.legend()

    #logarytm :c
    temp = 1
    U_log = []
    U_log_e = []
    I_log = []
    I_log_e = []
    while I[-temp] > -0.00002:
        U_log.insert(0, U[-temp])
        I_log.insert(0, I[-temp])
        I_log_e.insert(0, I_error[-temp])
        U_log_e.insert(0, U_error[-temp])
        temp += 1

    #fit logarytmiczny
    popt, pcov = curve_fit(log_fit, U_log, I_log)
    perr = np.sqrt(np.diag(pcov))

    a = popt[0]
    b = popt[1]
    a_err = perr[0]
    b_err = perr[1]

    wyniki['a_log\t[A]'] = a
    wyniki['a_log_error\t[A]'] = a_err
    wyniki['b_log\t[V]'] = b
    wyniki['b_log_error\t[V]'] = b_err

    wyniki['V_oc\t[V]'] = V_oc(a, b)
    wyniki['V_oc_error\t[V]'] = niepewnosc_V_oc(a, b, a_err, b_err)

    V_oc_list.append(wyniki['V_oc\t[V]'])
    V_oc_e.append(wyniki['V_oc_error\t[V]'])

    plt.plot(U_log, [log_fit(i, a, b) for i in U_log], c=LIGHT[index])
    plt.plot(wyniki['V_oc\t[V]'], 0, 'x', c=DARK[index], markersize=10)

    # zaokrąglenia
    I, I_error = zaokraglenie(I, I_error)
    U, U_error = zaokraglenie(U, U_error)

    divider = ['','','#','','']

    safe_file(U_lin + divider + U_log, U_lin_e + divider + U_log_e, I_lin + divider + I_log, I_lin_e + divider + I_log_e, 'Oświetlona ' + FILE_NAMES[index] + 'mA', wyniki)
#################################################################################################

Iy_part = I_sc_list[:4]
Ix = CURRENTS[:4]

# regresja liniowa
lin = linregress(Ix, Iy_part)

a = lin.slope
b = lin.intercept

plt.figure(2)
plt.errorbar(CURRENTS, I_sc_list, I_sc_e, CURRENTS_ERROR, '.', c="#ca6702")
plt.plot(CURRENTS, [a*i + b for i in CURRENTS], c='#C4803C', label='%.2g·I_LED + %.2g' % (a, b))
plt.xlabel('I LED [A]')
plt.ylabel('I zwarcia [A]')
plt.title('Zależność prądu zwarcia od natężenia prądu LED')
plt.legend()
##################################################################################################

popt, pcov = curve_fit(log_fit, CURRENTS, V_oc_list)
perr = np.sqrt(np.diag(pcov))

a = popt[0]
b = popt[1]

random_list = range(4, 41, 1)
plt.figure(3)
plt.plot(CURRENTS, V_oc_list, '.', c="#005f73")
plt.errorbar(CURRENTS[::3], V_oc_list[::3], V_oc_e[::3], CURRENTS_ERROR[::3], '.', c="#005f73")
plt.plot(random_list, [log_fit(i, a, b) for i in random_list], c="#65B4C4", label='%.2gln(I_LED)+%.2g'%(a,b))
plt.xlabel('I LED [A]')
plt.ylabel('V rozwarcia [V]')
plt.title('Zależność napięcia rozwarcia od natężenia prądu LED')
plt.legend()

safe_file(CURRENTS, CURRENTS_ERROR, I_sc_list, I_sc_e, "Prądy zwarcia", {})
safe_file(CURRENTS, CURRENTS_ERROR, V_oc_list, V_oc_e, "Napięcia rozwarcia", {})

plt.show()
