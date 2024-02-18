import matplotlib.pyplot as plt

V10 = open("10V.txt", 'r')
data_10 = []
lam_10 = []

for i in V10.readlines():
    i = i.rstrip('\n')
    i = i.split('\t')
    lam_10.append(float(i[0]))
    data_10.append(float(i[1]))

V10.close()

lam10e_file = open('10lam_error.txt', 'r')
lam10e = [float(i.rstrip('\n')) for i in lam10e_file.readlines()]
lam10e_file.close()

error10_file = open('10error.txt', 'r')
error10 = [float(i.rstrip('\n')) for i in error10_file.readlines()]
error10_file.close()

plt.figure()
plt.errorbar(lam_10, data_10, error10, lam10e, '.', c='#606c38', label='10V')
plt.ylabel("Napięcia termopary [V]")
plt.xlabel("Długość fali [um]")
plt.title("Porównanie odczytanego napięcia dla napięcia lampy 10V i 19V")



###########################################################################


V19 = open("19V.txt", 'r')
data_19 = []
lam_19 = []

for i in V19.readlines():
    i = i.rstrip('\n')
    i = i.split('\t')
    lam_19.append(float(i[0]))
    data_19.append(float(i[1]))
V19.close()

lam19e_file = open('19lam_error.txt', 'r')
lam19e = [float(i.rstrip('\n')) for i in lam19e_file.readlines()]
lam19e_file.close()

error19_file = open('19error.txt', 'r')
error19 = [float(i.rstrip('\n')) for i in error19_file.readlines()]
error19_file.close()

plt.errorbar(lam_19, data_19, error19, lam19e, '.', c='#bc6c25', label='19V')
plt.legend()

plt.show()
