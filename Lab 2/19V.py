import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from math import sqrt


def plancks_law(wavelength, temperature, A):
    """
    Planck's law function.

    Parameters:
        wavelength (float): Wavelength (in meters).
        temperature (float): Temperature of the black body (in Kelvin).
        A (float): Amplitude constant.

    Returns:
        float: Spectral radiance.
    """
    h = 6.62607004e-34  # Planck's constant (m^2 kg / s)
    c = 2.998e8         # Speed of light (m/s)
    k = 1.38064852e-23  # Boltzmann constant (m^2 kg / (s^2 K))

    return A * (2 * h * c**2 / wavelength**5) / (np.exp((h * c) / (wavelength * k * temperature)) - 1)


def fit_plancks_law(wavelengths, radiance):
    """
    Fit data to Planck's law.

    Parameters:
        wavelengths (array-like): Array of wavelengths (in meters).
        radiance (array-like): Array of spectral radiance.

    Returns:
        tuple: Optimal parameters and covariance matrix.
    """
    initial_guess = [2400, 2e-9]  # Initial guess for the amplitude constant

    params, covariance = curve_fit(plancks_law, wavelengths, radiance, p0=initial_guess)

    return params, covariance

##################################################################################################
##################################################################################################

# odczytanie danych pomiarowych
dane = open("19V.txt", 'r')

wavelengths = np.empty(1)
data = np.empty(1)

for line in dane.readlines():
    line = line.rstrip('\n')
    line = line.split("\t")
    wavelengths = np.append(wavelengths, float(line[0]) * 10 ** (-6))
    data = np.append(data, float(line[1]))

dane.close()

wavelengths = np.delete(wavelengths, 0)
data = np.delete(data, 0)

#znalezienie maximum danych
data_max = max(data)

#ustalenie indexu największej wartości
max_index = np.where(data == data_max)
max_index = max_index[0][0]

#normalizacja pomiarów
norm_data = data/data_max

# fitowanie
params, covariance = fit_plancks_law(wavelengths, data)

#normalizacja fitu
norm_fit = plancks_law(wavelengths, params[0], 1)
norm_fit = norm_fit/max(norm_fit)

#odczytanie z pliku niepewności lambdy
lam19e_file = open('19lam_error.txt', 'r')
lam19e = [float(i.rstrip('\n'))*10**(-6) for i in lam19e_file.readlines()]
lam19e_file.close()

#odczytanie z pliku niepewności pomiaru
error19_file = open('19error.txt', 'r')
error19 = [float(i.rstrip('\n')) for i in error19_file.readlines()]
error19_file.close()

#obliczenie niepewności znorwalizowanego pomiaru
error_norm = [sqrt( (error19[i] / data_max)**2 + (data[i] * error19[max_index]/data_max**2)**2) for i in range(len(error19))]


"""
#zapisywanie niepewności do pliku
en = open('error_norm_19V.txt', 'w')
[en.write(str(i) + '\n') for i in error_norm]
en.close()
"""

#wykres
plt.figure()
plt.errorbar(wavelengths, norm_data, error_norm, lam19e, '.', c='#ff7f0e', label='Dane pomiarowe')
#plt.scatter(wavelengths, norm_data)
plt.ylabel('Intensywność [a.u.]')
plt.xlabel('Długość fali [m]')
plt.title("Dopasowanie danych pomiarowych rozkładem Plancka dla napięcia 19V")

plt.plot(wavelengths, norm_fit, label = "Dopasowanie rozkładem Plancka")
plt.legend()

#plt.show()


#prawo wiena
b = 2.897771955 * 10**(-3)
l_max = wavelengths[max_index]
T = b/l_max

u_T = lam19e[max_index] * T / l_max
print(f"Temperatura włókna żarówki dla 19V: {T} +- {u_T}")