import nltk, time, sys, os, json
from tqdm import tqdm
sys.path.append('utils')
import asserts, utils

# Read command line arguments
# python subproject1/preprocess_text.py --path "./data" -o "./output/block1.json"
args = asserts.init_params()

if not os.path.isdir("output"):
    os.makedirs("output")
else:
    os.replace("output", "output")

try:
    nltk.data.find('tokenizer/punkt')
except:
    nltk.download('punkt')

def build_postings_list(block):
    dictionary = dict()
    for pairs in block:
        docID = int(pairs[0])
        term = pairs[1]

        if term not in dictionary:
            dictionary[term] = [1, set([docID])]
        elif term in dictionary:
            dictionary[term][1].add(docID)
            dictionary[term][0] = len(dictionary[term][1])

    for term in dictionary:
        dictionary[term][1] = sorted(list(dictionary[term][1]))

    raw = json.dumps(dictionary)
    with open('output/postings_list.json', 'a') as fp:
        fp.write(str(raw))
        fp.write("\n")

def preprocess_reuters(path):
    print("\nGeting raw files...")
    raw_files = utils.block_reader(path)
    print("\nParsing documents...")
    documents = utils.block_document_segmenter(raw_files)
    print("\nBuilding id-raw document pairs...")
    doc_pairs = utils.block_extractor(documents)

    print("\nCreating blocks...")
    for block in tqdm(utils.block_tokenizer(doc_pairs)):
        build_postings_list(block)
        
    return F

for reuters_file_content in tqdm(preprocess_reuters(args.path)):
    asserts.output(reuters_file_content)