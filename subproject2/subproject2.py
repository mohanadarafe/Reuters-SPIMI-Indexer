import nltk, time, sys, os, json
from collections import OrderedDict, defaultdict 
from tqdm import tqdm
from heapq import merge
sys.path.append('utils')
import asserts, utils

args = asserts.init_params()

def ranked_index(path):
    assert os.path.isfile("postings_list.json"), "Make sure you run subproject1 first! Check README for instructions."
    print("Parsing tokens")
    raw_files = utils.block_reader(path)
    documents = utils.block_document_segmenter(raw_files)
    doc_pairs = utils.block_extractor(documents)

    print("\nCalculating document average length")
    L_ave = utils.doc_length_average(doc_pairs)
    
    with open("postings_list.json", 'r') as f:
        data = f.read()
    
    print("\nCalculating RSV per document")
    inverted_index = json.loads(data)
    document_rsv = dict()
    doc_number = 1
    sum = 0
    for document in tqdm(doc_pairs):
        tf_id_dict = utils.build_tf_id(document)
        for tokens, tf in tf_id_dict.items():
            df = inverted_index[tokens][0]
            L_d = len(tf_id_dict)
            sum += utils.compute_rsv(df, tf, L_d, L_ave)

        document_rsv[doc_number] = format(sum, '.2f')
        sum = 0
        doc_number += 1
    
    raw = json.dumps(document_rsv, sort_keys=True, indent=4)
    with open('rsv.json', 'w') as fp:
        fp.write(str(raw))

ranked_index(args.path)