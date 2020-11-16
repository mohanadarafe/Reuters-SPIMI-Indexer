import nltk, glob, math, os, json, re
from nltk import word_tokenize
from tqdm import tqdm

def open_dictionary_file(file):
    assert os.path.isfile(file), "The file does not exist!"
    dictionary = dict()
    with open(file, 'r') as json_file: 
        dictionary = json.load(json_file)

    return dictionary

def get_tokens(document):
    tokensList = []
    for tokens in getDocumentTitle(document).split(" "):
        if tokens and "&" not in tokens:
            tokensList.append(tokens.rstrip('.,"'))

    for tokens in getDocumentBody(document).split(" "):
        if tokens and "&" not in tokens:
            tokensList.append(tokens.rstrip('.,"'))

    for tokens in getDocumentExtraTokens(document).split(" "):
        if tokens and "&" not in tokens:
            tokensList.append(tokens.rstrip('.,"'))

    return tokensList

def sanitizer(document, starterDelimiter, endDelimiter, index):
    query = r"(?=\S*[\'-])([a-zA-Z\'-]+)|(\w+)"
    start = document.find(starterDelimiter) + index
    end = document.find(endDelimiter)
    return start, end, query

def getDocumentBody(document):
    start, end, query = sanitizer(document, "<BODY>", "Reuter &#3;</BODY></TEXT></REUTERS", 6)
    final_data = ' '.join(i for i in document[start:end].split('\n') if re.findall(query, i))
    return final_data

def getDocumentTitle(document):
    start, end, query = sanitizer(document, "<TITLE>", "</TITLE>", 7)
    final_data = ' '.join(i for i in document[start:end].split('\n') if re.findall(query, i))
    return final_data

def getDocumentDate(document):
    start, end, query = sanitizer(document, "<DATELINE>", "</DATELINE>", 10)
    final_data = ' '.join(i for i in document[start:end].split('\n') if re.findall(query, i))
    return final_data

## This gets all tokens in <D> tags which includes people, categories & places.
def getDocumentExtraTokens(document):
    start, end, query = sanitizer(document, "<D>", "</D>", 3)
    final_data = ' '.join(i for i in document[start:end].split('\n') if re.findall(query, i))
    return final_data

def getDocumentId(document):
    start = document.find('NEWID="') + 7
    end = document.find(">", start) - 1
    return document[start:end]

def get_scores_from_postings(postings, rsv_scores):
    scores = []
    for docID in postings:
        scores.append((docID , float(rsv_scores[str(docID)])))
    scores = sorted(scores, key = lambda x: x[1])
    
    top = 10 if (len(scores) > 10) else len(scores)
    print(f'The top {top} documents are:')
    for i in range(top):
        print(f'{i+1}. Document {scores[i][0]}')

def idf(N, df):
    return math.log(N/df)

def _numerator(k, tf):
    return tf * (1+k)

def _denominator(k, b, L_d, L_ave, tf):
    product1_1 = 1-b
    product1_2 = b * (L_d / L_ave)
    product = k * (product1_1 + product1_2)
    return product + tf

def compute_rsv(df, tf, Ld, Lave, b=0, k=1) -> float:
    N = 21578
    product1 = idf(N, df)
    product2 = _numerator(k, tf) / _denominator(k, b, Ld, Lave, tf)
    return product1 * product2

def doc_length_average(document_dict):
    sum = 0
    for dictionary in tqdm(document_dict):
        tokens = get_tokens(dictionary["TEXT"])
        sum += len(tokens)
    return sum / 21578

def get_document_tf_id(dictionary, document):
    for tokens in get_tokens(document):
        if tokens not in dictionary:
            dictionary[tokens] = 1
        else:
            dictionary[tokens] += 1
    return dictionary

def build_tf_id(document_dict):
    tf_id = dict()
    text = document_dict["TEXT"]
    tf_id = get_document_tf_id(tf_id, text)
    return tf_id

def block_tokenizer(document_dict, flag = False):
    tupleList = []
    wordTuple = ()

    for dictionary in tqdm(document_dict):
        id = dictionary["ID"]
        text = dictionary["TEXT"]
        for words in get_tokens(text):
            if words != "":
                wordTuple = (id, words)
                tupleList.append(wordTuple)
            
    return tupleList

def block_extractor(documents):
    newsList = []
    newsDictionary = {}

    for document in tqdm(documents):
        newsDictionary = {'ID': getDocumentId(document), 'TEXT': document}
        newsList.append(newsDictionary)
        
    return newsList

def block_document_segmenter(raw_files):
    document_list = []
    document = ""
    keepCopying = False
    START_DELIMITER = '<REUTERS '
    END_DELIMITER = '</REUTERS>'
    
    for files in raw_files:
        for lines in tqdm(files.splitlines()):
            if END_DELIMITER in lines: 
                document += lines
                document_list.append(document)
                document = ""
                keepCopying = False
            if START_DELIMITER in lines: 
                keepCopying = True
            if keepCopying:
                document += " " + lines

    return document_list

def block_reader(path):
    fileContent = []
    try:
        files = []
        for file in glob.glob(path+"/*.sgm"):
            files.append(file)
        
        files.sort()

        for fileName in tqdm(files):
            raw = open(fileName, 'r', errors='ignore').read()
            fileContent.append(raw)
        
    except FileNotFoundError:
        print("File not found!")
    
    return fileContent