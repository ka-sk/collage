from math import sqrt
import matplotlib.pyplot as plt
from scipy.stats import linregress
from numpy import log

h = 4.13567E-15  # eV * s
c = 299792458  # m / s

q = 1.602176634E-19
k = 1.380649E-23
T = 300

#####################################################################################################################
def niepewnosc_U(U):
    return (0.0005*U+0.003)/sqrt(3)


def niepewnosc_I(I):
    return (0.005*I+0.0003)/sqrt(3)


def niepewnosc_Vbi(a, b, del_a, del_b):
    return sqrt(((del_a*b/a**2)**2) + (del_b/a)**2)


def V_bi(a, b):
    return -b/a


def Eg(lam):
    return h*c/lam

def niepewnosc_I_log(I, I_err):
    return I_err/I if I!=0 else 0

def niepewnosc_n(a, del_a):
    q = 1.602176634E-19
    k = 1.380649E-23
    T = 300
    return q*del_a/(k*T*a**2)


def niepewnosc_Rs_prim(V1, V2, u_V1, u_V2, I, u_I):
    return sqrt((u_V1/I)**2 + (u_V2/I)**2 + ((V1-V2) * u_I / I**2)**2)


def Rs_prim(V1, V2, I0):
    return abs(V1-V2)/I0

def wspolczynnik_idealnosci(a):
    return q/(k*T*a)


def Rs(a):
    return 1/a


def niepewnosc_Rs(a, a_err):
    return a_err/(a*a)

######################################################################################################################

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


def safe_file(x: list, x_err: list, y: list, y_err: list, name: str, additional:dict):
    file = open(r'Wyniki_obliczeń/ciemne/' + name + '.txt', 'w')

    [file.writelines(str(x[nr]) + "\t" + str(x_err[nr]) + "\t" + str(y[nr]) + "\t" + str(y_err[nr]) + "\n") for nr in range(len(x))]

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
            d[key[:-6]], d[key] = zaokraglenie(d[key[:-6]], d[key]) # WHAT THE FUCK IS WRONG HERE
    return d

#############################################################################################################


FILE_NAMES = ["germanowa","krzemowa"]

TYTULY = ['germanowej', 'krzemowej']

COLORS =['#c9ada7', '#4a4e69']

LIGHT_COLORS = ["#E0D0CC","#888CAA"]

DARK_COLORS = ["#AA7E74","#3B3E54"]

wyniki = {}


for index in range(len(FILE_NAMES)):
    U, I = read_file('Better/ciemne/' + FILE_NAMES[index] + '.txt')

    # sprowadzenie jednostek do SI podstawowych
    U = [i * 10**(-3) for i in U]  # V
    I = [i * 10**(-3) for i in I]  # A

    # obliczenie niepewności ze wzoru
    I_error = [niepewnosc_I(i) for i in I]  # A
    U_error = [niepewnosc_U(i) for i in U]  # V

    #zaokrąglenia
    I, I_error = zaokraglenie(I, I_error)
    U, U_error = zaokraglenie(U, U_error)


    #wybranie części danych do zaznaczenia niepewności na wykresie
    step = int(len(U)/11)
    U_part = [U[i] for i in range(0, len(U), step)]
    Ue_part = [U_error[i] for i in range(0, len(U), step)]
    I_part = [I[i] for i in range(0, len(U), step)]
    Ie_part = [I_error[i] for i in range(0, len(U), step)]

    #wykres
    plt.figure(index*3 + 1)
    plt.axhline(0, linestyle='--', c='#d6ccc2')
    plt.plot(U, I, '.', c=COLORS[index])
    plt.errorbar(U_part, I_part, Ie_part, Ue_part, '.', c=COLORS[index])
    plt.xlabel('U [V]')
    plt.ylabel('I [A]')
    plt.title("Charakterystyka prądowo-napięciowa nieoświetlonej diody " + TYTULY[index])

    # nadpisanie wycinków danych aby posłużyć się nimi do regresji liniowej
    U_part = U[-20:]
    I_part = I[-20:]
    Ue_part = U_error[-20:]
    Ie_part = I_error[-20:]

    # regresja liniowa
    lin = linregress(U_part, I_part)

    a = lin.slope
    b = lin.intercept
    a_err = lin.stderr
    b_err = lin.intercept_stderr

    # obliczenie potencjału wbudowanego
    Vbi = V_bi(a, b)
    Vbi_error = niepewnosc_Vbi(a, b, a_err, b_err)

    # zaznaczenie prostej na wykresie
    plt.plot([Vbi, U[-1]], [Vbi*a+b, U[-1]*a + b], c=LIGHT_COLORS[index], label='%.2f · U + %.2f' % (a, b))
    plt.plot(Vbi, 0, 'x', c=DARK_COLORS[index], markersize=10)
    plt.annotate("V_bi", (Vbi+0.02, 0.001))
    plt.legend()

    wyniki['a_Vbi\t[A/V]'] = a
    wyniki['a_Vbi_error\t[A/V]'] = a_err
    wyniki['b_Vbi\t[A]'] = b
    wyniki['b_Vbi_error\t[A]'] = b_err

    wyniki["Vbi\t[V]"] = Vbi
    wyniki['Vbi_error\t[V]'] = Vbi_error
    wyniki['Rs\t[Ohm]'] = Rs(a)
    wyniki['Rs_error\t[Ohm]'] = niepewnosc_Rs(a, a_err)

    safe_file(U_part, Ue_part, I_part, Ie_part, 'Dioda '+ FILE_NAMES[index], wyniki)

    ########################################################################################################
    #część od rezystancji

    I_log = [log(i) if i!=0 else 1 for i in I ]

    I_log_error = [niepewnosc_I_log(I[i], I_error[i]) for i in range(len(I))]

    #obcięcie danych pomiarowych, które były równe zero oraz dawały bullshit
    while -11.512925464970229 in I_log:
        i = I_log.index(-11.512925464970229)
        I_log.pop(i)
        I_log_error.pop(i)
        I_error.pop(i)
        U.pop(i)
        U_error.pop(i)
    
    while 1 in I_log:
        i = I_log.index(1)
        U.pop(i)
        I_log.pop(i)
        I_log_error.pop(i)
        I_error.pop(i)
        U_error.pop(i)


    #wzięcie części danych do leglinpa!
    U_part = U[:int(len(U)/7)]
    I_log_part = I_log[:int(len(I_log)/7)]
    I_log_part_error = I_log_error[:int(len(I_log)/7)]
    U_part_error = U_error[:int(len(I_log)/7)]

    # regresja liniowa
    lin = linregress(U_part, I_log_part)

    a = lin.slope
    b = lin.intercept
    a_err = lin.stderr
    b_err = lin.intercept_stderr

    wyniki['współczynnik idealności'] = wspolczynnik_idealnosci(a)
    wyniki['współczynnik idealności_error'] = niepewnosc_n(a, a_err)

    U_lin = [(i-b)/a for i in I_log]

    plt.figure(3*index + 3)
    plt.plot(U, I_log, '.', c=COLORS[index])
    plt.plot(U_lin, I_log, c=DARK_COLORS[index], label='%.2f · U + %.2f' % (a, b))
    plt.xlabel('U [V]')
    plt.ylabel('ln(I) [a.u.]')
    plt.axhline(max(I_log), c='#d6ccc2', linestyle='--')
    plt.title('Charakterystyka I-V w skali półlogarytmicznej diody ' + TYTULY[index])
    plt.legend()

    #znalezienie I0 max
    I_index = I_log.index((max(I_log)))
    V_lin = U_lin[I_index]
    V_U = U[I_index]
    V_lin_e = U_error[I_index]
    V_U_e = U_error[I_index]

    wyniki['a_log\t[1/V]'] = a
    wyniki['a_log_error\t[1/V]'] = a_err
    wyniki['b_log\t[a.u.]'] = b
    wyniki['b_log_error\t[a.u]'] = b_err
    wyniki["Rs_prim\t[Ohm]"] = Rs_prim(V_lin, V_U, max(I))
    wyniki["Rs_prim_error\t[Ohm]"] = niepewnosc_Rs_prim(V_lin, V_U, V_lin_e, V_U_e, max(I), I_error[I_index])
    wyniki['V1\t[V]'] = V_lin
    wyniki['u(V1)\t[V]'] = V_lin_e
    wyniki['V2\t[V]'] = V_U
    wyniki['u(V2)\t[V]'] = V_U_e
    wyniki['I_0\t[A]'] = max(I)
    wyniki['I_0_error\t[A]'] = I_error[I_index]

    plt.hlines(max(I_log), V_lin, V_U, colors=DARK_COLORS[index])
    plt.annotate("ΔV", (V_lin, max(I_log)-0.3))

    # zapisanie do pliku
    safe_file(U_part, U_part_error, I_log_part, I_log_part_error, 'Dioda ' + FILE_NAMES[index] + " log", wyniki)
    

plt.show()

