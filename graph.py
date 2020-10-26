#!/usr/bin/python3
# -*-coding:Utf-8 -*

# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np

def graph(data, theta_0, theta_1):
    # plt.axes = (0, max(data, key=lambda x:x['km'])['km'], \
        # 0, max(data, key=lambda x:x['price'])['price']])
    plt.axes = ([min(data, key=lambda x:x['km'])['km'], max(data, key=lambda x:x['km'])['km'], \
        min(data, key=lambda x:x['price'])['price'], max(data, key=lambda x:x['price'])['price']])
    # axes = plt.gca()
    # axes.set_xlim([-2.0, 2.0])
    # axes.set_ylim([min(small_results) - 0.5, max(small_results) + 0.5])
    plt.axhline(0, color='grey')
    plt.axvline(0, color='grey')
    plt.xlabel('km')
    plt.ylabel('price')
    plt.title('Linear Regression')
    
    # 100 linearly spaced numbers
    x = np.linspace(min(data, key=lambda x:x['km'])['km'], max(data, key=lambda x:x['km'])['km'], 100)
    y = theta_0 + theta_1 * x
    
    # On affiche les points du data set
    for row in data:
        plt.scatter(row['km'], row['price'], c='purple')

    # On affiche la droite avec les valeurs de theta trouvées
    plt.plot(x, y, linestyle='-', label="price = {} {} * km".format(round(theta_0, 2), round(theta_1, 2)))
    
    # plt.legend(loc="lower left")
    plt.show()