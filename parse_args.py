#!/usr/bin/python3
# -*-coding:Utf-8 -*
import argparse

def range_limited_float_type(arg):
    """ Type function for argparse - a float within some predefined bounds """
    try:
        f = float(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Learning rate must be a floating point number")
    if f < 0.0001 or f > 1:
        raise argparse.ArgumentTypeError("Learning rate must be between 0.0001 1")
    return f

def limited_float_type_precision(arg):
    """ Type function for argparse - a float within some predefined bounds """
    try:
        p = float(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Precision must be a floating point number")
    if p < 0.00000001 or p > 1:
        raise argparse.ArgumentTypeError("Precision must be between 0.00000001 and 1")
    return p

def positive_int_type(arg):
    """ Type function for argparse - a int that must be positive or null """
    try:
        nb = int(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be an integer")
    if nb < 0:
        raise argparse.ArgumentTypeError("Argument must be an int, positive or null")
    return nb

def parse_arguments():
    parser = argparse.ArgumentParser(usage='python3 %(prog)s [-h] [-s] [-g | -a] [-i ITERATION] [-l LEARNING_RATE] [-p PRECISION]', description="Linear regression with gradient descent in order to have correct results with predict.py")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-s", "--square", help="does the linear regression with the least square method, only '-g' option available", action="store_true")
    group.add_argument("-g", "--graph", help="open a graph representing the data", action="store_true")
    group.add_argument("-a", "--animation", help="display the evolution of the graph during the gradient descent", action="store_true")
    parser.add_argument("-i", "--iteration", help="Maximum number of iteration for gradient descent", type=positive_int_type, default=2147483647)
    parser.add_argument('-l', '--learning_rate', help="Learning rate for gradient descent, must be between 0 and 1", type=range_limited_float_type, default=0.01)
    parser.add_argument('-p', '--precision', help="Precision of the algorithm", type=limited_float_type_precision, default=0.00000001)
    return parser.parse_args()
