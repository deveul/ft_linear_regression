#!/usr/bin/python3
# -*-coding:Utf-8 -*

import json
import csv
import argparse
import copy

from graph import graph
from animation_rl import animation_rl

class Train:
    def __init__(self):
        self.data = self.get_data()
        self.normalized_data = None
        self.min_price = 0
        self.min_km = 0
        self.max_price = max(self.data, key=lambda x:x['price'])['price']
        self.max_km = max(self.data, key=lambda x:x['km'])['km']
        self.theta_0 = 0
        self.theta_1 = 0
        self.history_gradient = []
        self.learning_rate = 0.001

    def get_data(self):
        with open('data.csv', 'r') as data_file:
            data_reader = csv.DictReader(data_file)
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
            # self.data[i]['price'] = (self.data[i]['price'] - self.min_price) / (self.max_price - self.min_price)
            self.normalized_data[i]['price'] = self.data[i]['price']
            self.normalized_data[i]['km'] = (self.data[i]['km'] - self.min_km) / (self.max_km - self.min_km)
    
    def denormalize_data(self):
        for i, _ in enumerate(self.data):
            # self.data[i]['price'] = self.data[i]['price'] * (self.max_price - self.min_price) + self.min_price
            self.data[i]['km'] = self.data[i]['km'] * (self.max_km - self.min_km) + self.min_km
    
    def dump_theta_values(self):
        theta_values = {
            'theta_0': self.theta_0,
            'theta_1': self.theta_1
        }
        print(theta_values)
        with open('value_lr.json', 'w') as json_file:
            json.dump(theta_values, json_file)
            print("value_lr.json updated !")

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
        while True:
            sum_zero = self.calculate_sum_zero()
            sum_one = self.calculate_sum_one()
            
            gradient_zero = sum_zero * self.learning_rate
            gradient_one = sum_one * self.learning_rate
    
            self.theta_0 -= gradient_zero
            self.theta_1 -= gradient_one
    
            if animation and ((i < 1000 and i % 10 == 0) or (i < 10000 and i % 100 == 0) or (i % 1000 == 0)):
                self.history_gradient.append((self.theta_0, self.theta_1 / self.max_km))
            i += 1

            if abs(gradient_zero) < 0.00001 and abs(gradient_one) < 0.00001:
                break

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", help="open a graph representing the data", action="store_true")
    parser.add_argument("-a", "--animation", help="display the evolution of the graph during the gradient descent", action="store_true")
    return parser.parse_args()

def main():
    args = parse_arguments()
    train = Train()
    train.normalize_data()
    train.train(args.animation)
    train.theta_1 = train.theta_1 / train.max_km
    # train.theta_0 = train.theta_0 * train.max_price
    # train.theta_1 = train.theta_1 * train.max_price / train.max_km 
    # train.denormalize_data()
    if args.graph:
        graph(train.data, train.theta_0, train.theta_1)
    if args.animation:
        animation_rl(train.data, train.history_gradient)
    train.dump_theta_values()

if __name__ == "__main__":
    main()