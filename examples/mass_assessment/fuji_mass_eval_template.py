#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json

# That is how a request may look like (from the swagger API)
#curl -X POST "http://localhost:1071/fuji/api/v1/evaluate" -H  "accept: application/json" -H  "Authorization: Basic bWFydmVsOndvbmRlcndvbWFu" -H  "Content-Type: application/json" -d "{\"object_identifier\":\"https://archive.materialscloud.org/record/2021.146\",\"test_debug\":true,\"use_datacite\":true}"

results_folder = './results/'
# pids = ['https://archive.materialscloud.org/record/2021.146']

# or load pids from a file with one pid per line, which you have to generate beforehand
# Lines starting with '#' will be skipped as comments
# Normal lines are expected to have two fields separated by a space. For instance:
# 10.1234/XXYYZZ MyDataset
# The first field will be the PID and the second one the name of the dataset. This will be
# used to store the results in a way that can be easily recognised
with open('dois.txt', 'r') as fileo:
    pids = fileo.readlines()

fuji_api_url = 'http://localhost:1071/fuji/api/v1/evaluate'
# the Authorization key you get from your running swagger API instance
headers = {
    'accept': 'application/json',
    'Authorization': 'Basic bWFydmVsOndvbmRlcndvbWFu',
    'Content-Type': 'application/json'
}
base_request_dict = {'object_identifier': None, 'test_debug': True, 'use_datacite': True}

# Store one file per pid for later report creation
for pid_name in pids:
    # Skip lines with comments
    if pid_name.startswith('#'):
        continue
    aux = pid_name.split()
    pid = aux[0]
    # depending on the pid you may want to change this
    name = aux[1] if len(aux) > 1 else pid.split('/')[-1]
    req_dict = base_request_dict.copy()
    req_dict['object_identifier'] = pid
    req = requests.post(fuji_api_url, json=req_dict, headers=headers)

    rs_json = req.json()
    res_filename = '{}.json'.format(name)
    res_filename_path = os.path.join(results_folder, res_filename)

    with open(res_filename_path, 'w', encoding='utf-8') as fileo:
        json.dump(rs_json, fileo, ensure_ascii=False)
