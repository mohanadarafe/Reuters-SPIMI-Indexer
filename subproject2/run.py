from subprocess import *

Popen('python subproject2/subproject2.py --path "./data"', shell=True).wait()
print("\nThe ranked retrieval index is ready!\n")
query = input("Please enter a query: ")
while(not query): 
    print("Please enter a valid query")
    query = input("Please enter a query: ")
Popen(f'python subproject2/query.py --q "{query}"', shell=True).wait()