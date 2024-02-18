from math import sqrt
import matplotlib.pyplot as plt
from scipy.stats import linregress

h = 4.13567E-15  # eV * s
c = 299792458  # m / s

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

def Rs(a):
    return 1/a

def niepewnosc_Rs(a, a_err):
    return a_err/(a*a)

#h*c/lambs[index]

#h*c*u_lambs/(lambs[index]**2)

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
    file = open(r'Wyniki_obliczeń/Elektroluminescencyjne/' + name + '.txt', 'w')

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

#######################################################################################################################


FILE_NAMES = ["czerwona 660nm",
         "podczerwona 940nm",
         "pomarańczowa 620nm",
         "zielona 575nm",
         "żółta 585nm"]
TYTULY = ["czerwona 660.0±2.9nm",
         "podczerwona 940.0±2.9nm",
         "pomarańczowa 620.0±2.9nm",
         "zielona 575.0±2.9nm",
         "żółta 585.0±2.9nm"]

COLORS =['#E76F51', '#6C210F', '#F4A261', '#2A9D8F', '#E9C46A']

LIGHT_COLORS = ["#f0a693","#a23216","#f8c8a0","#3eccbb","#f2dca6"]

DARK_COLORS = ["#e24d28","#361107","#ef852e","#1e7167","#e3b33b"]

lambs = [660E-9, 940E-9, 620E-9, 575E-9, 585E-9]

u_lambs = 5E-9/sqrt(3)

wyniki = {}

plt.figure(1)

for index in range(len(FILE_NAMES)):
    U, I = read_file('Better/elektrolum/' + FILE_NAMES[index] + '.txt')

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
    plt.plot(U, I, '.', c=COLORS[index], label=TYTULY[index])
    plt.errorbar(U_part, I_part, Ie_part, Ue_part, '.', c=COLORS[index])
    plt.axhline(0, c='#d6ccc2', linewidth=0.3)
    plt.xlabel('U [V]')
    plt.ylabel('I [A]')
    plt.title('Charakterystyki prądowo-napięciowe badanych diód')
    plt.legend()

    # nadpisanie wycinków danych aby posłużyć się nimi do regresji liniowej
    U_part = U[-20:]
    I_part = I[-20:]
    Ie_part = I_error[-20:]
    Ue_part = U_error[-20:]

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
    plt.plot([Vbi, U[-1]], [Vbi*a+b, U[-1]*a + b], c=LIGHT_COLORS[index])
    plt.plot(Vbi, 0, 'x', color=DARK_COLORS[index], markersize=10)

    wyniki['a\t[A/V]'] = a
    wyniki['a_error\t[A/V]'] = a_err
    wyniki['b\t[A]'] = b
    wyniki['b_error\t[A]'] = b_err

    wyniki["Vbi\t[V]"] = Vbi
    wyniki['Vbi_error\t[V]'] = Vbi_error

    wyniki['Eg_hc\t[eV]'] = h*c/lambs[index]
    wyniki['Eg_hc_error\t[eV]'] = h*c*u_lambs/(lambs[index]**2)

    wyniki['lambda\t[m]'] = lambs[index]
    wyniki['lambda_error\t[m]'] = u_lambs

    wyniki['Rs\t[Ohm]'] = Rs(a)
    wyniki['Rs_error\t[Ohm]'] = niepewnosc_Rs(a, a_err)


    # zapisanie do pliku
    safe_file(U_part, Ue_part, I_part, Ie_part, 'Dioda '+ FILE_NAMES[index], wyniki)

plt.show()

