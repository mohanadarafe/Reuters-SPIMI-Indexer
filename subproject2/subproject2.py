import nltk, sys, os, json, time, string
from collections import OrderedDict
from tqdm import tqdm
sys.path.append('utils')
import asserts, utils

tf_dict_list = []
args = asserts.init_params()

def single_term_query(query: str, inverted_index: dict, rsv_scores: dict):
    if query in inverted_index:
        postings = inverted_index[query][1]
        utils.get_scores_from_postings(postings, rsv_scores)
    else:
        print(f"The query term \"{query}\" is not in the corpus!")

def and_term_query(query_terms: str, inverted_index: dict, rsv_scores: dict):
    postings_of_query_terms = []
    terms = query_terms.split()

    for query in terms.split(" "):
        if query in inverted_index:
            postings_of_query_terms.append(inverted_index[query][1])
        else:
            print(f"The query term \"{query}\" is not in the corpus!")

    and_postings = set.intersection(*[set(docID) for docID in postings_of_query_terms])
    utils.get_scores_from_postings(and_postings, rsv_scores)

def or_term_query(query_terms: str, inverted_index: dict, tf_dict: list):
    postings_of_query_terms = []
    terms = query_terms.split()

    for query in terms:
        if query in inverted_index:
            postings_of_query_terms.append(inverted_index[query][1])
        else:
            print(f"The query term \"{query}\" is not in the corpus!")

    or_postings = set.union(*[set(docID) for docID in postings_of_query_terms])
    tf_frequency = []
    for docs in or_postings:
        for query in terms:
            if query in tf_dict[docs-1]:
                tf_frequency.append((docs, tf_dict[docs-1][query]))

    utils.get_scores_from_or_query(tf_frequency)
    
def parse_query(query, queryType):
    assert len(tf_dict_list) == 21578, "Make sure you have all your reuters documents!"
    assert os.path.isfile("postings_list.json"), "Make sure you run subproject1 first! Check README for instructions."
    assert os.path.isfile("rsv.json"), "Make sure you run subproject2 first! Check README for instructions."
    inverted_index = utils.open_dictionary_file("postings_list.json")
    rsv_scores = utils.open_dictionary_file("rsv.json")

    start = time.time()
    if queryType == "1":
        assert len(query.split(" ")) == 1, "You have demanded a SINGLE query but you have more than one term."
        single_term_query(query, inverted_index, rsv_scores)
    elif queryType == "2":
        assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
        and_term_query(query, inverted_index, rsv_scores)
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
    
    print("\nCalculating RSV per document")
    inverted_index = utils.open_dictionary_file("postings_list.json")
    document_rsv = dict()
    doc_number = 1
    sum = 0
    for document in tqdm(doc_pairs):
        tf_id_dict = utils.build_tf_id(document)
        for tokens, tf in tf_id_dict.items():
            if tokens in inverted_index: 
                df = inverted_index[tokens][0]
            else: 
                continue
            L_d = len(tf_id_dict)
            sum += utils.compute_rsv(df, tf, L_d, L_ave)

        tf_dict_list.append(tf_id_dict)
        document_rsv[doc_number] = format(sum, '.2f')
        sum = 0
        doc_number += 1
    
    raw = json.dumps(document_rsv, sort_keys=True, indent=4)
    with open('rsv.json', 'w') as fp:
        fp.write(str(raw))

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