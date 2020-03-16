import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

    
#carico il file

with open("Dati5000.txt") as f:
    data = f.read()

data = data.split('\n')

del data[0] #rimuovo intestazione

N = [int(row.split('\t')[0]) for row in data]
epsilon = [float(row.split('\t')[1]) for row in data]
iterazioni = [int(row.split('\t')[2]) for row in data]
tempoiterazione = [float(row.split('\t')[3]) for row in data]
Overlap = [float(row.split('\t')[4]) for row in data]


plt.figure(1);    
plt.plot(epsilon, Overlap, 'b +')
plt.xlabel('epsilon');
plt.ylabel('Overlap');

plt.figure(2);    
plt.plot(epsilon, iterazioni, 'b +')
plt.xlabel('epsilon');
plt.ylabel('Numero iterazioni');

with open("Dati5000_x.txt") as f:
    data = f.read()

data = data.split('\n')

del data[0] #rimuovo intestazione

N = [int(row.split('\t')[0]) for row in data]
epsilon = [float(row.split('\t')[1]) for row in data]
iterazioni = [int(row.split('\t')[2]) for row in data]
tempoiterazione = [float(row.split('\t')[3]) for row in data]
Overlap = [float(row.split('\t')[4]) for row in data]


plt.figure(1);
bluepatch = mpatches.Patch('blue', label='N=5000')
redpatch = mpatches.Patch('red', label='N=10000')
plt.legend(handles=[bluepatch, redpatch])
plt.plot(epsilon, Overlap, 'b +')
plt.xlabel('epsilon');
plt.ylabel('Overlap');

plt.figure(2);
bluepatch = mpatches.Patch('blue', label='N=5000')
redpatch = mpatches.Patch('red', label='N=10000')
plt.legend(handles=[bluepatch, redpatch])
plt.plot(epsilon, iterazioni, 'b +')
plt.xlabel('epsilon');
plt.ylabel('Numero iterazioni');

with open("Dati10000.txt") as f:
    data = f.read()

data = data.split('\n')

del data[0] #rimuovo intestazione

N = [int(row.split('\t')[0]) for row in data]
epsilon = [float(row.split('\t')[1]) for row in data]
iterazioni = [int(row.split('\t')[2]) for row in data]
tempoiterazione = [float(row.split('\t')[3]) for row in data]
Overlap = [float(row.split('\t')[4]) for row in data]


plt.figure(1);    
plt.plot(epsilon, Overlap, 'r x')
plt.xlabel('epsilon');
plt.ylabel('Overlap');

plt.figure(2);    
plt.plot(epsilon, iterazioni, 'r x')
plt.xlabel('epsilon');
plt.ylabel('Numero iterazioni');

with open("Dati10000_x.txt") as f:
    data = f.read()

data = data.split('\n')

del data[0] #rimuovo intestazione

N = [int(row.split('\t')[0]) for row in data]
epsilon = [float(row.split('\t')[1]) for row in data]
iterazioni = [int(row.split('\t')[2]) for row in data]
tempoiterazione = [float(row.split('\t')[3]) for row in data]
Overlap = [float(row.split('\t')[4]) for row in data]


plt.figure(1);    
plt.plot(epsilon, Overlap, 'r x')

plt.figure(2);    
plt.plot(epsilon, iterazioni, 'r x')

Y=np.linspace(-10, 250, 1000)
X=[0.268]*1000


plt.figure(1);    
plt.plot(X, Y, 'k .')

plt.figure(2);    
plt.plot(X, Y, 'k .')

plt.show()



