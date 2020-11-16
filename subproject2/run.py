from subprocess import *
import time

Popen('python subproject2/subproject2.py --path "./data"', shell=True).wait()
print("\nThe ranked retrieval index is ready!\n")

keepGoing = True
while (keepGoing):
    queryType = input("Please enter a query type: [1] SINGLE [2] AND [3] OR: ")
    while(queryType not in ["1", "2", "3"]): 
        print("Please enter a valid query type")
        queryType = input("Please enter a query type: [1] SINGLE [2] AND [3] OR: ")

    query = input("Please enter a query: ")
    while(not query): 
        print("Please enter a valid query type")
        queryType = input("Please enter a query type: ")

    Popen(f'python subproject2/query.py --q "{query}" --t "{queryType}"', shell=True).wait()

    inp = input("Would you like to submit another query? [y/n] ")
    while(inp not in ["y", "n"]):
        print("Please enter a valid response")
        inp = input("Would you like to submit another query? [y/n] ")

    keepGoing = True if inp == "y" else False

print("Thank you!")
print("SPIMI Indexer - Written by Mohanad Arafe")