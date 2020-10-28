#!/usr/bin/python3
# -*-coding:Utf-8 -*

# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np

def graph(data, theta_0, theta_1):
    axes = plt.gca()
    plt.axhline(0, color='grey')
    plt.axvline(0, color='grey')
    plt.xlabel('km')
    plt.ylabel('price')
    plt.title('Linear Regression')
    
    # 100 linearly spaced numbers
    x = np.linspace(min(data, key=lambda x:x['km'])['km'], max(data, key=lambda x:x['km'])['km'], 100)
    y = theta_0 + theta_1 * x
    
    # On affiche les points du data set
    plt.scatter([x['km'] for x in data], [y['price'] for y in data], c='purple', label='Values of data set')

    # On affiche la droite avec les valeurs de theta trouvées
    plt.plot(x, y, linestyle='-', label="price = {} {} * km".format(round(theta_0, 2), round(theta_1, 2)))
    
    axes.set_ylim(bottom=0)
    axes.set_xlim(left=0)
    plt.legend(loc="lower center")
    plt.show()