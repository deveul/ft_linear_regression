#!/usr/bin/python3
# -*-coding:Utf-8 -*

import json
import csv
import copy
from statistics import mean
import numpy as np

from graph import graph
from animation_lr import animation_lr
from parse_args import parse_arguments

class Train:
    def __init__(self, iteration, learning_rate, precision):
        self.data = self.get_data()
        self.normalized_data = None
        self.min_price = 0
        self.min_km = 0
        self.max_price = max(self.data, key=lambda x:x['price'])['price']
        self.max_km = max(self.data, key=lambda x:x['km'])['km']
        self.theta_0 = 0
        self.theta_1 = 0
        self.history_gradient = []
        self.learning_rate = learning_rate
        self.iteration = iteration
        self.precision = precision

    def get_data(self):
        with open('data.csv', 'r') as data_file:
            data_reader = csv.DictReader(data_file)
            headers = data_reader.fieldnames
            if 'km' not in headers:
                print("km column is missing")
                exit()
            if 'price' not in headers:
                print("price column is missing")
                exit()
            if len(headers) > 2:
                print("Too many columns in csv, there should be only two (km and price).")
                exit()
            
            data = list(data_reader)
            try :
                data = [dict([key, float(value)] for key, value in row.items()) for row in data]
            except :
                print("Seems that there is something wrong in the csv file")
                exit()

            return data
    
    def normalize_data(self):
        self.normalized_data = copy.deepcopy(self.data)
        for i, _ in enumerate(self.normalized_data):
            self.normalized_data[i]['price'] = (self.data[i]['price'] - self.min_price) / (self.max_price - self.min_price)
            self.normalized_data[i]['km'] = (self.data[i]['km'] - self.min_km) / (self.max_km - self.min_km)
    
    def dump_theta_values(self):
        theta_values = {
            'theta_0': self.theta_0,
            'theta_1': self.theta_1
        }
        try:
            with open('value_lr.json', 'w') as json_file:
                json.dump(theta_values, json_file)
                print("value_lr.json updated:\n\ttheta_0: {}\n\ttheta_1: {}".format(self.theta_0, self.theta_1))
        except PermissionError:
            print("Vous n'avez pas les droits pour écrire dans le fichier value_lr.json")
            exit()

    def get_estimated_price(self, km):
        return self.theta_0 + self.theta_1 * km
    
    def calculate_sum_zero(self):
        sum_zero = 0
        for row in self.normalized_data:
            km = row['km']
            price = row['price']
            sum_zero += self.theta_1 * km + self.theta_0 - price
        return sum_zero / len(self.normalized_data)
    
    def calculate_sum_one(self):
        sum_one = 0
        for row in self.normalized_data:
            km = row['km']
            price = row['price']
            sum_one += (self.theta_1 * km + self.theta_0 - price) * km
        return sum_one / len(self.normalized_data)

    def train(self, animation):
        i = 0
        while i < self.iteration:
            sum_zero = self.calculate_sum_zero()
            sum_one = self.calculate_sum_one()
            
            gradient_zero = sum_zero * self.learning_rate
            gradient_one = sum_one * self.learning_rate
    
            self.theta_0 -= gradient_zero
            self.theta_1 -= gradient_one
    
            if animation and ((i < 1000 and i % 10 == 0) or (i < 10000 and i % 100 == 0) or (i % 1000 == 0)):
                self.history_gradient.append((self.theta_0 * self.max_price, self.theta_1 * self.max_price / self.max_km))
            i += 1

            if abs(gradient_zero) < self.precision and abs(gradient_one) < self.precision:
                break
        self.theta_0 = self.theta_0 * self.max_price
        self.theta_1 = self.theta_1 * self.max_price / self.max_km 

    def train_with_least_square(self):
        x = np.float_([x['km'] for x in self.data])
        y = np.float_([x['price'] for x in self.data])
        n = len(x)   
        m_x, m_y = mean(x), mean(y)
        Somme_xy = sum(y*x) - n*m_y*m_x
        Somme_xx = sum(x*x) - n*m_x*m_x
        a = Somme_xy / Somme_xx
        b = m_y - a*m_x  
        self.theta_0 = b
        self.theta_1 = a


def main():
    args = parse_arguments()
    train = Train(args.iteration, args.learning_rate, args.precision)
    if args.square:
        train.train_with_least_square()
    else :
        train.normalize_data()
        train.train(args.animation)
        if args.animation:
            animation_lr(train.data, train.history_gradient)
    if args.graph:
        graph(train.data, train.theta_0, train.theta_1)
    train.dump_theta_values()

if __name__ == "__main__":
    main()