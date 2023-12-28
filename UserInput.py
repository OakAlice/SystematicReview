# User input and code initialisation page

from itertools import product

# enter the keywords to search for where each row is a concept with synonyms
A1 = ['accelerometer', 'IMU'] # base
A2 = ['activity', 'behaviour',] # synonyms
A3 = ['machine learning', 'classification'] # synonyms
B = ['wildlife', 'animal'] # synonyms
C = ['unsupervised', 'clustering'] # synonyms

# define the concept combinations you'd want to search for
combinations_a = list(product(A1, A2, A3, B)) # animal (probably supervised)
combinations_b = list(product(A1, A2, A3, B, C)) # animal unsupervised

# they're added together to form one list
search_strings = combinations_a + combinations_b

# the parent directory where the results should be saved (they'll go into individual database folders)
output_directory = "C:/Users/oakle/Documents/PhD docs/Systematic Results/DecemberRedo"

# number of articles per search from each of the strings
Num_of_articles = 100

# API keys
ScopusKey = 'fdbb42b4b0363feb81cf4551863b0279' # Elsevier's Scopus Search API
PubMedEmail = 'oaw001@student.usc.edu.au' # PubMed email account
COREKey = "XXXX" # for CORE Api
SemanticKey = 'XBlMKbMLsO1pCQSj9zbQDaW7MrGOSvlS9OGo6cko' # for Semantic Scholar

# The script is now ready to run

# import the functions from each of the individual scripts

from ScholarStringsToUrl import generate_scholar_urls
from SearchScholar2 import QueryScholar
#from TidyScholar import TidyingScholarResults

from SearchScopus import QueryScopus
from SearchPubMed import QueryPubMed
#from SearchArXiv import QueryArxiv
#from SearchCORE import QueryCore
from SearchScienceDirect import QueryScienceDirect

from Combining import CombiningDatabases
from GettingAbstracts import get_abstracts

# call and run all the scripts with these variables
def main():
    urls = generate_scholar_urls(search_strings)
    QueryScholar(urls, Num_of_articles, output_directory)
    #TidyingScholarResults(output_directory)
    
    #QueryScopus(ScopusKey, search_strings, output_directory, Num_of_articles)
    #QueryPubMed(search_strings, Num_of_articles, output_directory, PubMedEmail)
    #QueryArxiv(search_strings, Num_of_articles, output_directory)
    #QueryCore(output_directory, search_strings, COREKey, Num_of_articles)
    #QuerySemantic(search_strings, offset=0, limit=Num_of_articles)
    #QueryScienceDirect(search_strings, Num_of_articles, ScopusKey, output_directory)
        
    #CombiningDatabases(output_directory)
    #get_abstracts(output_directory, PubMedEmail)

if __name__ == "__main__":
    main()

# you should now have a csv file with lots of relevant papers and their info
