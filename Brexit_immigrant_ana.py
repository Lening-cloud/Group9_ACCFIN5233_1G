import re  # for regex
from collections import Counter  # for counting word freq
from wordcloud import WordCloud  # for generate wordcloud pic
import matplotlib  # for drawing pic

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import os
# import nltk
# # nltk.download('wordnet')
# # nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()
year = '2021'

# privative words
NEGWORDS = ["not", "no", "none", "neither", "never", "nobody", "n't", 'nor']
# stopwords = ["an", "a", "the"] + NEGWORDS
STOPWORDS = ["an", "a", "the", "or", "and", "thou", "must", "that", "this", "self", "unless", "behind", "for", "which",
             "whose", "can", "else", "some", "will", "so", "from", "to", "by", "within", "of", "upon", "th", "with",
             "it", "say", "ha", "wa", "one"] + NEGWORDS


# Delete from txt all words contained in STOPWORDS.
def _remove_stopwords(words):
    for i, word in enumerate(words):
        if word in STOPWORDS:
            words[i] = " "
    return words


# Decompose doc into array of words
def decompose_word(doc):
    txt = doc.split()
    return txt


# Count number of each word in one doc
def wordcount(words, dct):
    counting = Counter(words)
    count = []
    for key, value in counting.items():
        if key in dct:
            count.append([key, value])
    return count


# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


############## BEGIN read content & pre-process content ####################
brexit_string = ''

rootdir = 'doc_' + year
list = os.listdir(rootdir)
for i in range(len(list)):
    # path表示"根路径+rootdir+list[i]"，也就是第i个文件的完整根路径
    path = os.path.join(rootdir, list[i])
    with open(path, 'r', encoding='utf-8') as brexit_read:
        content = brexit_read.read()
        if 'immigrant' or 'migration' or 'emigration' in content:
            brexit_string += content
            brexit_string += '\n'


############## END read content & pre-process content ####################


############## BEGIN NLP ####################
brexit_split = str.split(brexit_string, sep=',')

# split token
tokens = []
for k in brexit_split:
    # 1. regex cleaning
    cleantextprep = str(k)
    expression = "[^a-zA-Z ]"  # keep only letters, numbers and whitespace
    cleantextCAP = re.sub(expression, '', cleantextprep)  # apply regex
    cleantext = cleantextCAP.lower()  # lower case

    # 2. token
    tokens_temp = decompose_word(cleantext)
    tagged_sent = pos_tag(tokens_temp)

    # 3. lemmatizer
    for i in range(len(tokens_temp)):
        # ADJ, ADJ_SAT, ADV, NOUN, VERB
        word_type = get_wordnet_pos(tagged_sent[i][1]) or wordnet.NOUN
        if word_type == wordnet.ADJ or wordnet.NOUN or wordnet.VERB :
            tokens_temp[i] = lemmatizer.lemmatize(tokens_temp[i], pos=word_type)
        else:
            tokens_temp[i] = ''

    # 4. remove stop words
    tokens_temp_without_stop_words = _remove_stopwords(tokens_temp)

    # 5. add to total result
    tokens.extend(tokens_temp_without_stop_words)

# word count
nwords = len(tokens)  # Number of words in article

# wordcloud
comment_words = ' ' + ' '.join(tokens) + ' '
wordcloud = WordCloud(width=1600, height=1000,
                      background_color='black',
                      min_font_size=10).generate(comment_words)
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig("result_immigrant_{}/wordcloud_{}.png".format(year,year), format='png', dpi=500)
plt.show()

############## END NLP ####################


############## BEGIN sentimental ####################
### Read in BL lexicon
# Negative lexicon
ndct = ''
with open('bl_negative.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        ndct = ndct + line
# create a list of negative words
ndct = ndct.split('\n')
len(ndct)

# Positive lexicon
pdct = ''
with open('bl_positive.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        pdct = pdct + line
pdct = pdct.split('\n')
len(pdct)

# negative & positive word count
nwc = wordcount(tokens, ndct)
pwc = wordcount(tokens, pdct)

# Total number of positive/negative words
ntot, ptot = 0, 0
for i in range(len(nwc)):
    ntot += nwc[i][1]

for i in range(len(pwc)):
    ptot += pwc[i][1]


with open('result_immigrant_{}/Posi_{}.txt'.format(year,year), 'w+') as f:
    posi_num = '{} words in {} article data'.format(nwords, year) +'\n'
    posi_num += 'Total number of positive words: ' + str(ptot) + '\n'
    for i in range(len(pwc)):
        posi_num += (str(pwc[i][0]) + ': ' + str(pwc[i][1])) + '\n'
    posi_num += ('Percentage of positive words: ' + str(round(ptot / nwords, 4)))
    f.write(posi_num)

with open('result_immigrant_{}/Nega_{}.txt'.format(year,year), 'w+') as f:
    nega_num = '{} words in {} article data'.format(nwords, year) + '\n'
    nega_num += 'Total number of negative words: ' + str(ntot) + '\n'
    for i in range(len(nwc)):
        nega_num += (str(nwc[i][0]) + ': ' + str(nwc[i][1])) + '\n'
    nega_num += ('Percentage of negative words: ' + str(round(ntot / nwords, 4)))
    f.write(nega_num)

############## END sentimental ####################