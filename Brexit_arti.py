import json
from lxml import etree
import requests

# 1. Get the page by url
# use sleep if need, if HTTP 429/404/500 happens
def proceed_url(web_url):
    response = requests.get(web_url)
    content = response.content
    return content

# 2. Positioning section
# content=dom.path('//*[@id="story"]/section')
# 3. parsing p in section
# dom.xml()
def proceed_html(html_content):
    full_content = ''

    xml_dom = etree.HTML(html_content)
    dom_section = xml_dom.xpath('//*[@id="story"]/section//p')
    for i in range(len(dom_section)):
        # text content of the i-th paragraph in this article
        paragraph_content = dom_section[i].text

        if paragraph_content != None:
            full_content += '\n'
            full_content += paragraph_content

    return full_content

# 4. write to file
def write_to_file(file_name, content):
    with open(file_name,'w+') as f:
        f.write(content)
    return


############################################################

# 0.1
# gain url from json
file = open('Brexit_2016.json', 'r')
lines = file.readlines()
# for each page
for i in range(len(lines)):
    line_object = json.loads(lines[i])
    line_docs = line_object['response']['docs']

    # for every doc in this page
    for ii in range(len(line_docs)):
        doc_object = line_docs[ii]
        web_url = doc_object['web_url']
        # 1.
        html_content = proceed_url(web_url)
        # 2.3.
        doc_content = proceed_html(html_content)
        # 4.
        write_to_file('doc_2016/{}-{}'.format(i, ii), doc_content)


############ end ################

