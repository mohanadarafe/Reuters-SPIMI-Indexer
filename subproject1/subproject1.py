import nltk, time, sys, os, json
from collections import OrderedDict, defaultdict 
from tqdm import tqdm
from heapq import merge
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

def read_block_from_disk(blockFile: str) -> dict:
    dictionary = dict()
    with open(f"output/{blockFile}", 'r') as json_file: 
        dictionary = json.load(json_file)

    return dictionary

def write_block_to_disk(dictionary: dict, blockNumber: int):
    raw = json.dumps(dictionary)
    with open(f'output/block{blockNumber}.json', 'w') as fp:
        fp.write(str(raw))

def merge_blocks():
    inverted_index = OrderedDict()
    
    print("Merging blocks...")
    for blockfile in tqdm(os.listdir("output")):
        block = read_block_from_disk(blockfile)
        for key in block:
            postings = inverted_index[key] if key in inverted_index else set()
            doc_occurences = block[key][1]
            postings.update(doc_occurences)
            inverted_index[key] = postings

    print("Computing doc frequency...")
    for token in tqdm(inverted_index):
        sorted_doc_freq = sorted(inverted_index[token])
        doc_freq = len(sorted_doc_freq)
        inverted_index[token] = (doc_freq, sorted_doc_freq)

    raw = json.dumps(inverted_index)
    with open('postings_list.json', 'w') as f:
        f.write(str(raw))

def separate_blocks(path):
    print("\nGeting raw files...")
    raw_files = utils.block_reader(path)
    print("\nParsing documents...")
    documents = utils.block_document_segmenter(raw_files)
    print("\nBuilding id-raw document pairs...")
    doc_pairs = utils.block_extractor(documents)

    print("\nCreating blocks...")
    blockNumber = 1
    tokenNumber = 1
    dictionary = dict()
    BLOCK_SIZE = 500

    for block in tqdm(utils.block_tokenizer(doc_pairs)):
        build_postings_list(block, dictionary)

        if tokenNumber == 500:
            dictionary = sort_postings_list(dictionary)
            write_block_to_disk(dictionary, blockNumber)
            dictionary = dict() # reset the dictionary for the next block
            blockNumber += 1 
            tokenNumber = 0
        else: tokenNumber += 1

    # Dump the rest
    dictionary = sort_postings_list(dictionary)
    write_block_to_disk(dictionary, blockNumber)
    merge_blocks()

merge_blocks()