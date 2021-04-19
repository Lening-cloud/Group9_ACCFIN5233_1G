# -*- coding: utf-8 -*-
import json
import pandas as pd

with open('Brexit_2016.json', 'r') as json_file:
    lines = json_file.readlines()
    doc_dataframe = pd.DataFrame()
    for i in range(len(lines)):
        line_object = json.loads(lines[i])
        line_docs = line_object['response']['docs']

        doc_dataframe = doc_dataframe.append(pd.DataFrame(line_docs), ignore_index=True)
    doc_dataframe.to_csv('Brexit_2016.csv')