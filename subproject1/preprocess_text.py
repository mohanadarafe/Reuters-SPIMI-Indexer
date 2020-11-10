import nltk, time, sys, os, json
from collections import OrderedDict 
from tqdm import tqdm
sys.path.append('utils')
import asserts, utils

args = asserts.init_params()

def sort_postings_list(dictionary):
    return OrderedDict(sorted(dictionary.items()))

def build_postings_list(block, dictionary):
    docID = int(block[0])
    term = block[1]

    if term not in dictionary:
        dictionary[term] = [1, list(set([docID]))]
    elif (term in dictionary) and (docID not in dictionary[term][1]):
        dictionary[term][1].append(docID)
        dictionary[term][0] = len(dictionary[term][1])
        
    return dictionary

def preprocess_reuters(path):
    print("\nGeting raw files...")
    raw_files = utils.block_reader(path)
    print("\nParsing documents...")
    documents = utils.block_document_segmenter(raw_files)
    print("\nBuilding id-raw document pairs...")
    doc_pairs = utils.block_extractor(documents)

    print("\nCreating blocks...")
    blockNumber = 1
    dictionary = dict()
    for block in tqdm(utils.block_tokenizer(doc_pairs)):
        build_postings_list(block, dictionary)

        if len(dictionary) == 500:
            dictionary = sort_postings_list(dictionary)
            raw = json.dumps(dictionary)
            with open(f'output/block{blockNumber}.json', 'w') as fp:
                fp.write(str(raw))
            dictionary = dict()
            blockNumber += 1

    # Dump the rest
    raw = json.dumps(dictionary)
    with open(f'output/block{blockNumber}.json', 'w') as fp:
        fp.write(str(raw))

preprocess_reuters(args.path)