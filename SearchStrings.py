## Creating search strings
from itertools import product

# search terms I want to use, seperated into rows by synonyms
A1 = ['accelerometer'] # base
A2 = ['activity classification', 'behaviour classification', 'activity recognition'] # synonyms
A3 = ['machine learning', 'classification algorithm'] # synonyms
B = ['wildlife', 'animal'] # synonyms
C = ['unsupervised', 'clustering'] # synonyms
D = ['sport', 'sleep']

# the combinations I want to generate
combinations_A = list(product(A1, A2, A3)) # base human studies
combinations_AB = list(product(A1, A2, A3, B)) # animal (probably supervised)
combinations_AC = list(product(A1, A2, A3, C)) # human unsupervised
combinations_AD = list(product(A1, A2, A3, D)) # sport and sleep specific
long_combinations = list(product(A1, A2, A3, B, C)) # animal unsupervised

search_strings = combinations_A + combinations_AB + combinations_AC + combinations_AD + long_combinations