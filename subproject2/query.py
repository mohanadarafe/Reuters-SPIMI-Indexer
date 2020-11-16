import nltk, sys, os, json
from collections import OrderedDict
from tqdm import tqdm
sys.path.append('utils')
import asserts, utils

args = asserts.init_params()
query = args.query[0].split(" ")

assert os.path.isfile("postings_list.json"), "Make sure you run subproject1 first! Check README for instructions."
assert os.path.isfile("rsv.json"), "Make sure you run subproject2 first! Check README for instructions."

inverted_index = utils.open_dictionary_file("postings_list.json")
rsv_scores = utils.open_dictionary_file("rsv.json")

def single_term_query(query: str):
    if query in inverted_index:
        postings = inverted_index[query][1]
        scores = []
        for docID in postings:
            scores.append((docID , float(rsv_scores[str(docID)])))
        scores = sorted(scores, reverse=True)
        
        top = 10 if (len(scores) > 10) else len(scores)
        print(f'The top {top} documents are:')
        for i in range(top):
            print(f'Document {scores[i][0]}')

    else:
        print("The query term you input is not in the corpus!")
        exit()

def multi_term_query(query_terms: list):
    print(query_terms)

def parse_query():
    if len(query) == 1:
        single_term_query(query[0])
    else:
        multi_term_query(query)

parse_query()