import nltk, sys, os, json, time
from collections import OrderedDict
from tqdm import tqdm
sys.path.append('utils')
import asserts, utils

args = asserts.init_params()
query = args.query[0].split(" ")
queryType = args.type[0]

assert os.path.isfile("postings_list.json"), "Make sure you run subproject1 first! Check README for instructions."
assert os.path.isfile("rsv.json"), "Make sure you run subproject2 first! Check README for instructions."

inverted_index = utils.open_dictionary_file("postings_list.json")
rsv_scores = utils.open_dictionary_file("rsv.json")

def single_term_query(query: str):
    if query in inverted_index:
        postings = inverted_index[query][1]
        utils.get_scores_from_postings(postings, rsv_scores)
    else:
        print(f"The query term \"{query}\" is not in the corpus!")
        exit()

def and_term_query(query_terms: list):
    postings_of_query_terms = []
    for query in query_terms:
        if query in inverted_index:
            postings_of_query_terms.append(inverted_index[query][1])
        else:
            print(f"The query term \"{query}\" is not in the corpus!")
            exit()

    and_postings = set.intersection(*[set(docID) for docID in postings_of_query_terms])
    utils.get_scores_from_postings(and_postings, rsv_scores)

def or_term_query(query_terms: list):
    postings_of_query_terms = []
    for query in query_terms:
        if query in inverted_index:
            postings_of_query_terms.append(inverted_index[query][1])
        else:
            print(f"The query term \"{query}\" is not in the corpus!")
            exit()

    and_postings = set.union(*[set(docID) for docID in postings_of_query_terms])
    utils.get_scores_from_postings(and_postings, rsv_scores)

def parse_query():
    if queryType == "1":
        assert len(query) == 1, "You have demanded a SINGLE query but you have more than one term."
        single_term_query(query[0])
    elif queryType == "2":
        assert len(query) > 1, "You have demanded an AND query but you have only entered one term."
        and_term_query(query)
    elif queryType == "3":
        assert len(query) > 1, "You have demanded an AND query but you have only entered one term."
        or_term_query(query)

start = time.time()
parse_query()
end = time.time()
print(f'\nDone! Your query was found in {"{:.3f}".format(end-start)} seconds')