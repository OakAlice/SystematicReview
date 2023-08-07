## Creating search strings
from itertools import product

# each row is a concept to search for each column is a synonym for that concept
A1 = ['accelerometer'] # base
A2 = ['activity classification', 'behaviour classification', 'activity recognition'] # synonyms
A3 = ['machine learning', 'classification algorithm'] # synonyms
B = ['wildlife', 'animal'] # synonyms
C = ['unsupervised', 'clustering'] # synonyms
D = ['sport', 'sleep'] # additional specific fields I'd like to find

# define the concept combinations you'd want to search for
combinations_A = list(product(A1, A2, A3)) # base human studies
combinations_AB = list(product(A1, A2, A3, B)) # animal (probably supervised)
combinations_AC = list(product(A1, A2, A3, C)) # human unsupervised
combinations_AD = list(product(A1, A2, A3, D)) # sport and sleep specific
long_combinations = list(product(A1, A2, A3, B, C)) # animal unsupervised

# they're added together to form one big list
search_strings = combinations_A + combinations_AB + combinations_AC + combinations_AD + long_combinations

# other user inputs
# the parent directory where the results should be saved (they'll go into individual database folders)
output_directory = "C:/Users/oakle/OneDrive/Documents/Systematic Results"

# number of articles from each of the databases
PubMed_num_of_articles = 1000
Scholar_num_of_articles = 1000
Scopus_num_of_articles = 100