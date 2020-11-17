import nltk, sys, os, json, time, string
from collections import OrderedDict
from tqdm import tqdm
sys.path.append('utils')
import asserts, utils

tf_dict_list = []
L_average = []
args = asserts.init_params()

def single_term_query(query: str, inverted_index: dict, tf_dict: list):
    if query in inverted_index:
        postings = inverted_index[query][1]
        utils.get_scores_from_single_postings(postings, tf_dict, inverted_index, query, L_average[0])
    else:
        print(f"The query term \"{query}\" is not in the corpus!")

def and_term_query(query_terms: str, inverted_index: dict, tf_dict: list):
    postings_of_query_terms = []
    terms = query_terms.split()

    for query in terms:
        if query in inverted_index:
            postings_of_query_terms.append(inverted_index[query][1])
        else:
            print(f"The query term \"{query}\" is not in the corpus!")

    and_postings = set.intersection(*[set(docID) for docID in postings_of_query_terms])
    utils.get_scores_from_and_postings(and_postings, tf_dict, inverted_index, terms, L_average[0])

def or_term_query(query_terms: str, inverted_index: dict, tf_dict: list):
    postings_of_query_terms = []
    terms = query_terms.split()

    for query in terms:
        if query in inverted_index:
            postings_of_query_terms.append(inverted_index[query][1])
        else:
            print(f"The query term \"{query}\" is not in the corpus!")

    or_postings = set.union(*[set(docID) for docID in postings_of_query_terms])
    utils.get_scores_from_or_query(or_postings, tf_dict, terms)
    
def parse_query(query, queryType):
    assert len(tf_dict_list) == 21578, "Make sure you have all your reuters documents!"
    assert os.path.isfile("postings_list.json"), "Make sure you run subproject1 first! Check README for instructions."
    inverted_index = utils.open_dictionary_file("postings_list.json")

    start = time.time()
    if queryType == "1":
        assert len(query.split(" ")) == 1, "You have demanded a SINGLE query but you have more than one term."
        single_term_query(query, inverted_index, tf_dict_list)
    elif queryType == "2":
        assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
        and_term_query(query, inverted_index, tf_dict_list)
    elif queryType == "3":
        assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
        or_term_query(query, inverted_index, tf_dict_list)
    end = time.time()
    print(f'\nDone! Your query was found in {"{:.3f}".format(end-start)} seconds')

def ranked_index(path):
    assert os.path.isfile("postings_list.json"), "Make sure you run subproject1 first! Check README for instructions."
    print("Parsing tokens")
    raw_files = utils.block_reader(path)
    documents = utils.block_document_segmenter(raw_files)
    doc_pairs = utils.block_extractor(documents)

    print("\nCalculating document average length")
    L_ave = utils.doc_length_average(doc_pairs)
    L_average.append(L_ave)
    
    print("\nCalculating tf per document")
    inverted_index = utils.open_dictionary_file("postings_list.json")
    for document in tqdm(doc_pairs):
        tf_id_dict = utils.build_tf_id(document)
        tf_dict_list.append(tf_id_dict)

    keepGoing = True
    while (keepGoing):
        queryType = input("\nPlease enter a query type: [1] SINGLE [2] AND [3] OR: ")
        while(queryType not in ["1", "2", "3"]): 
            print("Please enter a valid query type")
            queryType = input("Please enter a query type: [1] SINGLE [2] AND [3] OR: ")

        query = input("Please enter a query: ")
        while(not query): 
            print("Please enter a valid query type")
            queryType = input("Please enter a query type: ")

        parse_query(query, queryType)

        inp = input("Would you like to submit another query? [y/n] ")
        while(inp not in ["y", "n"]):
            print("Please enter a valid response")
            inp = input("Would you like to submit another query? [y/n] ")

        keepGoing = True if inp == "y" else False

    print("Thank you!")
    print("SPIMI Indexer - Written by Mohanad Arafe")

ranked_index(args.path)