# -*- coding: utf-8 -*-
import json

with open('Brexit_2021.json', 'r') as json_file, open('Brexit_2021.csv', 'w+') as csv_file:
    lines = json_file.readlines()
    for i in range(len(lines)):
        line_object = json.loads(lines[i])
        line_docs = line_object['response']['docs']

        for ii in range(len(line_docs)):
            doc_object = line_docs[ii]
            web_url = doc_object['web_url']

            csv_file.write(web_url)
            csv_file.write('\n')