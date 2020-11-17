import nltk, time, sys, os, json
from collections import OrderedDict, defaultdict 
from tqdm import tqdm
from heapq import merge
sys.path.append('utils')
import asserts, utils

args = asserts.init_params()

def sort_postings_list(dictionary: dict) -> dict:
    '''
    The following function sorts a postings list 
    '''
    return OrderedDict(sorted(dictionary.items()))

def build_postings_list(block: tuple, dictionary: dict) -> dict:
    '''
    The following function inputs a (docID, term) tuple and a dictionary
    and returns the updated dictionary with the tuple.
    '''
    docID = int(block[0])
    term = block[1]

    if term not in dictionary:
        dictionary[term] = list(set([docID]))
    elif (term in dictionary) and (docID not in dictionary[term]):
        dictionary[term].append(docID)
        
    return dictionary

def read_block_from_disk(blockFile: str) -> dict:
    '''
    The following function inputs file name & loads the file content
    in a dictionary.
    '''
    return utils.open_dictionary_file(f"output/{blockFile}")
    
def write_block_to_disk(dictionary: dict, blockNumber: int):
    '''
    The following function inputs file name & a dictionary and write the 
    dictionary content in a file.
    '''
    raw = json.dumps(dictionary)
    with open(f'output/block{blockNumber}.json', 'w') as fp:
        fp.write(str(raw))

def merge_blocks():
    '''
    The following function merges the blocks in the output folder where each
    file is labelled as Block.json. It produces the postings list in the 
    root folder.

    Initially, it merges the blocks simply by considering the postings list
    without the document frequency. Once that is merged, we simply add the
    frequency and produce the tuple for our dictionary.
    '''
    inverted_index = OrderedDict()
    
    print("Merging blocks...")
    for blockfile in tqdm(os.listdir("output")):
        block = read_block_from_disk(blockfile)
        for key in block:
            postings = inverted_index[key] if key in inverted_index else set()
            doc_occurences = block[key]
            postings.update(doc_occurences)
            inverted_index[key] = postings

    print("Adding frequency...")
    for token in tqdm(inverted_index):
        sorted_doc_freq = sorted(inverted_index[token])
        doc_freq = len(sorted_doc_freq)
        inverted_index[token] = (doc_freq, sorted_doc_freq)

    raw = json.dumps(inverted_index, sort_keys=True, indent=4)
    with open('postings_list.json', 'w') as f:
        f.write(str(raw))

def SPIMI(path: str):
    '''
    The following function processes reuters files & separates blocks of
    500 tokens as it processes the data. The output is a merged postings list
    produced in the root directory.

    Initially, we parse the reuters documents, extract the (docID, term) tuples
    and for each 500 tokens, we produce its own block. Finally, once all blocks 
    are separated, we merge them together.
    '''
    print("\nGeting raw files...")
    raw_files = utils.block_reader(path)
    print("\nParsing documents...")
    documents = utils.block_document_segmenter(raw_files)
    print("\nBuilding id-raw document pairs...")
    doc_pairs = utils.block_extractor(documents)

    blockNumber = 1
    dictionary = dict()
    BLOCK_SIZE = 500
    tokenNumber = 1

    print("\nSeparating blocks...")
    for block in tqdm(utils.block_tokenizer(doc_pairs)):
        build_postings_list(block, dictionary)

        if tokenNumber == BLOCK_SIZE:
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
    print(f"Done! File created at: {os.path.abspath('postings_list.json')}")

SPIMI(args.path)