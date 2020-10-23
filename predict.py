#!/usr/bin/python3
# -*-coding:Utf-8 -*

import json

def get_user_input():
    tmp = input("Veuillez entrer le kilométrage de votre voiture ('q|quit' pour quitter):\n")
    try:
        kilometers = float(tmp)
        assert 0 <= kilometers
        return kilometers, True
    except ValueError:
        if tmp.lower() == 'quit' or tmp.lower() == 'q':
            return 'quit', True
        print("Vous n'avez pas saisi un nombre, veuillez réessayer")
        return tmp, False
    except AssertionError:
        print("Le kilométrage doit être supérieur ou égal à zéro")
        return tmp, False

def main():
    theta = None
    with open('value_lr.json', 'r') as json_file:
        theta = json.load(json_file)
    theta_0 = theta["theta_0"]
    theta_1 = theta["theta_1"]
    print("résolution avec theta_0={} et theta_1={}".format(theta_0, theta_1))
    keep_going = True
    while keep_going:
        input, valid = get_user_input()
        if valid:
            if input == 'quit':
                keep_going = False
            else:
                print("Prix estimé = {}".format(theta_0 + theta_1 * input))
        else:
            pass

if __name__ == "__main__":
    main()