Introduction
---------------------
This project contains python codes and sample data in year 2021 and belongs to Group9_ACCFIN5233_1G.

Project Structure
---------------------
Projects includes code and sample data. Function of codes will be shown below and we provide sample JSON and CSV data in year 2021. Corresponding result data is also provided in other folders.  

Run Method
---------------------
Please run codes below on sequence to get complete result. Basic shell code:
```shell
python3 {python file name}
```
python file name:
- Brexit_year.py:
This module will call New York Times API to download raw article list and write them to JSON file, with year number included in the name of each file. 
After executing, file with name Brexit_{yearNumber}.json will be created.

- Brexit_json2csv.py:
To make data more readily, we design this simple module, to transform raw JSON data into CSV file. Run then check file like Brexit_{yearNumber}.csv.

- Brexit_arti.py:
This file reads raw JSON data, parses to get URLs of the articles, downloads and extract the intact content of each article. 

- Brexit_immigrant_ana.py, Brexit_policy_ana.py, Brexit_text_ana.py
These are codes of analysis. Each of them will output some statistics file and wordcloud picture into folder result_{type}_{year}. 

