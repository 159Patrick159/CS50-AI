import os
import random
from pomegranate import *
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        print(sys.argv)
        print(len(sys.argv))
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Divide (1-Damping factor) for all the websites in the corpus
    random_link = (1-damping_factor)/len(corpus)
    prob_dist = {}
    # Check for links in current page
    if NumLinks(corpus,page):
        # Calculate probabilty of chosing link within page assuming pages has links
        link_num = NumLinks(corpus,page)
        link_probability = damping_factor/link_num
        for name in corpus[page]:
            # Update dictionary with the probabilty for each link
            prob_dist.update({name:(link_probability+random_link)})

    else:
        # If there are not outgoing links then we assume it has links to all pages
        link_probability = damping_factor/len(corpus)
        for name in corpus.keys():
            # Avoid adding same probability to current page
            if name == page:
                continue
            else:
                # Update dictionary with the probabilty for all other links
                prob_dist.update({page:(link_probability+random_link)})

    # Store all links in page in one list
    links = [link for link in corpus[page]]

    # Add probability of random page for those pages not within links list
    for page in corpus.keys():
        if page not in links: 
            prob_dist.update({page:random_link})
    # Return the probability distribution dictionary
    return(prob_dist)

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a list with all the pages in the corpus
    pages = [page for page in corpus.keys()]
    start_dict = {}
    # Create the starting discreate distribution
    for name in pages:
        # The distribution is equal for all sites
        start_dict.update({name:(1/len(corpus))})
    start = DiscreteDistribution(start_dict)
    conditonal_table = []
    for page in pages:
        # Obtain the transition model for current page
        conditional_prob = transition_model(corpus,page,damping_factor)
        for link in conditional_prob.keys():
            temp = []
            # Append origin page
            temp.append(page)
            # Append link inside page
            temp.append(link)
            # Append probability of link
            temp.append(conditional_prob[link])
            # Append list to table
            conditonal_table.append(temp)
    # Create the conditional probability table through pomegranate
    transition = ConditionalProbabilityTable(conditonal_table,[start])
    # Create the markov chain
    model = MarkovChain([start,transition])
    # Create empty dict where the probability of each sample will be
    sample_probability = {}
    # Create a model with sample size
    model_list = list(model.sample(n))
    for page in pages:
        # Count how many times the pages was visited in the model
        count = model_list.count(page)
        # Calculate the probabilty of surfer being in page
        prob = count/n
        sample_probability.update({page:prob})
    return(sample_probability)
        
def NumLinks(corpus, page):
    """
    Returns the number of links a page in a corpus has
    """
    page_links = corpus[page]
    num = len(page_links)
    return(num)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a list with all the pages in the corpus
    pages = [page for page in corpus.keys()]
    # Give all pages same starting probabilty
    page_prob = {}
    for page in pages:
        init_prob = 1/len(corpus)
        page_prob.update({page:init_prob})
    # Establish a threshold for min change in probability calc
    threshold = 0.001
    # Compute initial condition probability for overall PR
    cond1 = (1-damping_factor)/len(corpus)
    while True:
        for page_p in pages:
            sum_0 = 0
            for page_i in pages:
                # Ignore the same page
                if page_i == page_p:
                    continue
                # Check if page i has a link to page p
                if page_p in corpus[page_i]:
                    sum_0 = sum_0 + page_prob[page_i]/NumLinks(corpus,page_i)
            # Calculate the pagerank for page_p
            page_rank = cond1 + (damping_factor*sum_0)
            # Calculate the difference in the between both PR
            diff = abs(page_rank - page_prob[page_p])
            # If difference is smaller or equal to threshold we stop
            if diff <= threshold:
                return(page_prob)
            # Else we update the pagerank of that page
            else:
                page_prob.update({page_p:page_rank})
            

if __name__ == "__main__":
    main()
