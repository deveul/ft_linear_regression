#!/usr/bin/python3
# -*-coding:Utf-8 -*

import json
import csv
import argparse

from graph import graph

def dump_theta_values(theta_0, theta_1):
    theta_values = {
        'theta_0': theta_0,
        'theta_1': theta_1
    }
    print(theta_values)
    with open('value_lr.json', 'w') as json_file:
        json.dump(theta_values, json_file)
        print("value_lr.json updated !")

def get_data():
    with open('data.csv', 'r') as data_file:
        data_reader = csv.DictReader(data_file)
        data = list(data_reader)
        try :
            data = [dict([key, int(value)] for key, value in row.items()) for row in data]
        except :
            print("Seems that there is something wrong in the csv file")
            exit()
        return data

def get_theta():
    # theta = None
    # with open('value_lr.json', 'r') as json_file:
        # theta = json.load(json_file)
    return 0, 0
    # return theta["theta_0"], theta["theta_1"]

def estimated_price(km, theta_0, theta_1):
    return theta_0 + theta_1 * km

def get_ideal_ratio():
    return 0.1

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", help="open a graph representing the data", action="store_true")
    return parser.parse_args()

def main():
    args = parse_arguments()
    data = get_data()
    if args.graph:
        graph(data)
    theta_0, theta_1 = get_theta()
    m = len(data)
    somme = 0
    somme2 = 0
    for index, row in enumerate(data):
        m = index + 1
        r = get_ideal_ratio()
        somme += estimated_price(row['km'], theta_0, theta_1) - row['price']
        somme2 += (estimated_price(row['km'], theta_0, theta_1) - row['price']) * row['km']
        tmp_theta_0 = r * somme / m
        tmp_theta_1 = r * somme2 / m

        theta_0= tmp_theta_0
        theta_1 = tmp_theta_1
    dump_theta_values(theta_0, theta_1)

if __name__ == "__main__":
    main()