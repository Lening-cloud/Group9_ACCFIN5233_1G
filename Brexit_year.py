# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import requests
import time

endpoint = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

params = { 'api-key': 'x4mib2lUOFbjNF0PuKSbzFV3CseOhn9b',
           'q': 'brexit',
           'begin_date': '20160101',
           'end_date':'20161231'
           }


with open('Brexit_2016.json', 'w+') as f:
    for i in range(100):
        # set pagination parameter
        params['page'] = i
        if i%10==9:
            # sleep to avoid HTTP 500 error
            time.sleep(120)
        try:
            response = requests.get(endpoint, params)
            response.raise_for_status()
            result_num = len(response.json()['response']['docs'])
            print("this is page {}, result num is {}".format(i+1,result_num))
            if result_num == 0:
                break
            f.write(json.dumps(response.json()))
            f.write('\n')
        except Exception as ex:
            raise ex




