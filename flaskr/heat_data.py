from flask import request

import time
import requests
import csv

heat_data = []


def parse_data(file_name):
    file = open(file_name)
    csvreader = csv.reader(file)

    for h in csvreader:
        heat_data.append(h)

    return heat_data


def send_data(data, cage_id, sleepTime, url):
    while(True):
        index = 0
        for h in heat_data:
            if index == 0:
                index += 1
                continue
            payload = {'cage_id': cage_id, 'intensity': h[0], 'max_heat':h[1]}
            requests.post(url, data = payload)
            print(f'water updated: intensity: {h[0]}, max_heat: {h[1]}\n')
            time.sleep(sleepTime)

