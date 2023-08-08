# User input and code initialisation page

from itertools import product

# enter the keywords to search for where each row is a concept with synonyms
A1 = ['accelerometer'] # base
A2 = ['activity classification', 'behaviour classification', 'activity recognition'] # synonyms
A3 = ['machine learning', 'classification algorithm'] # synonyms
B = ['wildlife', 'animal'] # synonyms
C = ['unsupervised', 'clustering'] # synonyms
D = ['sport', 'sleep'] # additional specific fields

# define the concept combinations you'd want to search for
combinations_A = list(product(A1, A2, A3)) # base human studies
combinations_AB = list(product(A1, A2, A3, B)) # animal (probably supervised)
combinations_AC = list(product(A1, A2, A3, C)) # human unsupervised
combinations_AD = list(product(A1, A2, A3, D)) # sport and sleep specific
long_combinations = list(product(A1, A2, A3, B, C)) # animal unsupervised

# they're added together to form one list
search_strings = combinations_A + combinations_AB + combinations_AC + combinations_AD + long_combinations

# the parent directory where the results should be saved (they'll go into individual database folders)
output_directory = "C:/Users/oakle/OneDrive/Documents/Systematic Results"

# number of articles per search from each of the databases
PubMed_num_of_articles = 5
Scholar_num_of_articles = 10
Scopus_num_of_articles = 2

# API keys
ScopusKey = 'fdbb42b4b0363feb81cf4551863b0279' # Elsevier's Scopus Search API
PubMedEmail = 'oaw001@student.usc.edu.au' # PubMed email account

# The script is now ready to run

# import the functions from each of the individual scripts
from ScholarStringsToUrl import generate_scholar_urls
from SearchScholar2 import QueryScholar
from SearchScopus import QueryScopus
from SearchPubMed import QueryPubMed
from TidyScholar import TidyingScholarResults
from TidyScopus import TidyingScopusResults
from TidyPubMed import TidyingPubMedResults
from Combining import CombiningDatabases
from GettingAbstracts import get_abstracts

# call and run all the scripts with these variables
def main():
    #urls = generate_scholar_urls(search_strings)
    #QueryScholar(urls, Scholar_num_of_articles, output_directory)
    #QueryScopus(ScopusKey, search_strings, output_directory, Scopus_num_of_articles)
    #QueryPubMed(search_strings, PubMed_num_of_articles, output_directory, PubMedEmail)
    #TidyingScholarResults(output_directory)
    #TidyingScopusResults(output_directory)
    #TidyingPubMedResults(output_directory)
    #CombiningDatabases(output_directory)
    get_abstracts(output_directory, PubMedEmail)

if __name__ == "__main__":
    main()

