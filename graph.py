#!/usr/bin/python3
# -*-coding:Utf-8 -*

import matplotlib.pyplot as plt

def graph(data):
    plt.axes = ([0, max(data, key=lambda x:x['km']), 0, max(data, key=lambda x:x['km'])])
    # axes = plt.gca()
    # axes.set_xlim([-2.0, 2.0])
    # axes.set_ylim([min(small_results) - 0.5, max(small_results) + 0.5])
    plt.axhline(0, color='grey')
    plt.axvline(0, color='grey')
    for row in data:
        plt.scatter(row['km'], row['price'], c='purple')
    # plt.legend(loc="upper left")
    plt.xlabel('km')
    plt.ylabel('price')
    plt.title('Linear Regression')
    
    plt.show()