#! bin/python
import nltk
import os
import time

import argparse
import json

#utworzenie ścieżki dla pliku wyjściowego, do późniejszej poprawy
timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
outfile = "run{}.out".format(timestr)
#utworzenie ścieżki dla pliku wyjściowego, do późniejszej poprawy

#pobranie adresu pliku z wypisaną trasą
parser = argparse.ArgumentParser(description="")
parser.add_argument('trip_plan', help='Sciezka pliku z danymi wycieczki', type =str)
args = parser.parse_args()
#pobranie adresu pliku z wypisaną trasą

def load(path):
    with open(path, 'r') as file:
        return json.load(file)

def initialize_agents():
    pass

if __name__ == "__main__":
    #pobierz wejście
    trip_plan = load(args.trip_plan)

    #przeczytaj wejście
    trip = [v for k, v in trip_plan.items() if k == "points"]
    trip_points = [v for v in trip[0]]

    #dla wejścia wykonaj wywołaj agenty

    #odbierz od agentów i zapisz w pliku

