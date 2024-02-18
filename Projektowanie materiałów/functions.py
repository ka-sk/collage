import numpy as np


def stop(material1: dict or float, material2: dict or float, concentration: float, bowing=0.00):
    """
    :param material1: dane dla materiału pierwszego w postaci słownika lub pojedynczej wartości typu float
    :param material2: dane dla drugiego materiału, dla którego jest zdefiniowana koncentracja
    :param concentration: koncentracja drugiego materiału
    :param bowing: stała doświadczalna
    :return: stopu dwóch materiałów o podanej koncentracji
    """
    # jeżeli zmienne material są słownikami to zamykamy całość w pętlę i obliczamy ze wzoru dla każdego elementu słownika
    if type(material1) == dict:
           material3 = {}
           for key in material1.keys():
               # wzór na stop z uwzględnieniem bowingu gdzie koncentracja odnosi się do materiału 1
               material3[key] = concentration * material1[key] + (1 - concentration) * material2[
                   key] - concentration * (1 - concentration) * bowing


    # jeżeli zmienne material1 i material2 są liczbami to korzystamy po prostu ze wzoru
    elif type(material1) != str and type(material1) != bool:
        material3 = concentration * material1 + (1 - concentration) * material2 - concentration * (
                    1 - concentration) * bowing
    else:
        return None
    return material3


def conc(material1: float, material2: float, material3: float, bowing=0.00):
    """
    :param material1: dany parametr materiału, który chcemy zmieszać
    :param material2: parametr drugiego składnika stopu
    :param material3: parametr, który chcemy otrzymać w danym materiale
    :param bowing: stała doświadczalna
    :return: kocentracja material2 w material1 by otrzymać stop materiałów o parametrze material3
    """
    if bowing == 0:
        return (material3 - material2) / (material1 - material2)
        pass
    else:
        return (np.sqrt((bowing - material1 + material2) ** 2 - 4 * bowing * (material2 - material3)) + bowing - material1 + material2) / 2*bowing


def Eg_T(T, Eg_0, alpha, beta):
    """
    :param T: temperatura [K]
    :param Eg_0: przerwa energetyczna dla T=0K [eV]
    :param alpha: stała materiałowa [eV/K]
    :param beta: stała materiałowa [K]
    :return: energia przerwy energetycznej w danej temperaturze [eV]
    """

    return Eg_0 - ((alpha * T ** 2) / (beta + T))


def E_g_with_tension(E_0, a, eps):
    """
    :param E_0: energia poziomu energetycznego bez naprężeń [eV]
    :param a: stała materiałowa charakterystyczna dla danego pasma [eV]
    :param eps: odształcenie liniowe (ang. strain)
    :return: energia poziomu energetycznego z uwzględnieniem naprężenia [eV]
    """

    return a*eps + E_0


def epsilon(a_podloza, a_material):
    """
    :param a_podloza: stała krystaliczna dla podłoża struktury
    :param a_material: stała krystaliczna właściwego materiału
    :return: całkowite odształcenie liniowe (ang. strain) (pomnożone trzykrotnie,
    gdyż zakładamy takie samo odkształcenie we wszystkich kierunkach)
    """

    return 3 * (a_podloza - a_material) / a_material


def quantum_well(s: dict, o: dict, eps=0.00):
    """
    :param s: parametry materiału, z którego tworzymy studnię potencjału
    :param o: parametry materiału otoczenia
    :param eps: naprężenia materiału
    :return: krotka, składająca się z trzech list:
    lista argumentów na osi x,
    lista z wartościami energii dla pasma walencyjnego,
    lista z wartoścaimi energii dla pasma przewodnictwa
    krotka jest gotowa do przedstawienia na wykresie
    """

    # definicja wartości dla osi x
    os_x = [0, 1, 1, 2, 2, 3]

    # definicja zmiennych pomocniczych dla otoczenia studni
    o_v = o["VBO"]
    o_c = o["VBO"] + o["Eg"]

    # definicja zmiennych pomocniczych dla studni
    s_v = s["VBO"] - eps * s['a_v']
    s_c = s["VBO"] + s["Eg"] + eps * s['a_c']

    # definicja końcowych list
    VB = [o_v] * 2 + [s_v] * 2 + [o_v] * 2
    CB = [o_c] * 2 + [s_c] * 2 + [o_c] * 2

    return os_x, VB, CB
