# COMP 479 - Project 2

## Objective
Implement SPIMI. Implement ranking of returns. Test and analyze your system, discuss how your design decisions influence the results.

## Data
Use Reuters21578. For docID, use the NEWID values from the Reuters corpus to make your retrieval comparable

### Subproject I: Implement SPIMI using your Project 2 Subproject 1 system. In particular:
1. (Project 2 Subproject I item 1:) develop a module that while there are still more documents to be processed,
accepts a document as a list of tokens and outputs term-documentID pairs. Instead of appending new term-docID
pairs to a global list, do:
2. SPIMI: for 500 term-docIDs, create a new hash key for the term if necessary and/or append the docID to the
postings list associated with the hashed term
3. when the block is full (representing 500 term-docIDs), collect the index, sort, and ”store” in consecutively labelled
BlockX
4. disk block merging: when all term-docID pairs of your input are stored in block-sized indices, merge the dictionaries (the term and pointer) into a single index
5. compare timing with the naive indexer
6. compile an inverted index for Reuters21578 without using any compression techniques

### Sub-project 2: Convert your indexer into a probabilistic search engine
1. using the assumptions made in Chapter 11 about independence of terms and documents etc. and
2. using the BM25 formula (11.32),
3. rank the documents your SPIMI implementation returns and
4. for a given query, return a ranked list of results.

### Sub-project 3: Queries
1. design three test queries:
    (a) a single keyword query,
    (b) a multiple keywords query returning documents containing all the keyword(AND),
    (c) a multiple keywords query returning documents containing at least one keyword (OR), where documents are ordered by how many keywords they contain)
2. run your three test queries to showcase your code and comment on the results in your report

## Running the project

### Setup
Make sure you have Conda installed on your machine
```
conda env create --name project3 --file=environment.yml
conda activate project3
```