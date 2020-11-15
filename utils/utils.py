import nltk, glob
from nltk import word_tokenize
from tqdm import tqdm

def get_tokens(document):
    tokensList = []
    for tokens in getDocumentTitle(document):
        tokensList.append(tokens)

    for tokens in getDocumentBody(document):
        tokensList.append(tokens)

    for tokens in getDocumentExtraTokens(document):
        tokensList.append(tokens)

    return tokensList

def sanitizer(document, starterDelimiter, endDelimiter, index):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    start = document.find(starterDelimiter) + index
    end = document.find(endDelimiter)
    return start, end, tokenizer

def getDocumentBody(document):
    start, end, tokenizer = sanitizer(document, "<BODY>", "Reuter &#3;</BODY></TEXT></REUTERS", 6)
    tokens = tokenizer.tokenize(document[start:end])
    return tokens

def getDocumentTitle(document):
    start, end, tokenizer = sanitizer(document, "<TITLE>", "</TITLE>", 7)
    tokens = tokenizer.tokenize(document[start:end])
    return tokens

def getDocumentDate(document):
    start, end, tokenizer = sanitizer(document, "<DATELINE>", "</DATELINE>", 10)
    tokens = tokenizer.tokenize(document[start:end])
    return tokens

## This gets all tokens in <D> tags which includes people, categories & places.
def getDocumentExtraTokens(document):
    start, end, tokenizer = sanitizer(document, "<D>", "</D>", 3)
    tokens = tokenizer.tokenize(document[start:end])
    return tokens

def getDocumentId(document):
    start = document.find('NEWID="') + 7
    end = document.find(">", start) - 1
    return document[start:end]

def block_tokenizer(document_dict):
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

        #assert len(fileContent) == 22, "There may be a missing file!"
        
    except FileNotFoundError:
        print("File not found!")
    
    return fileContent