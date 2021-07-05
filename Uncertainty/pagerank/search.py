from googlesearch import search
query = input("Enter your query: ")
urls = search(query, num_results=10)
print(urls)