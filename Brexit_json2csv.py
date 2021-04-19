# -*- coding: utf-8 -*-
import json
import pandas as pd

with open('Brexit_2016.json', 'r') as json_file:
    js_content = json.loads(json_file)

    data_raw = pd.DataFrame(js_content)
    data_raw.set_index(keys = 'data', inplace = True)
    data_raw.to_csv('Brexit_2016.csv')