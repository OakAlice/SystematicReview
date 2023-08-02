## Creating search strings
from itertools import product

# search terms I want to use, seperated into rows by synonyms
A1 = ['accelerometer']
A2 = ['activity classification', 'behaviour classification', 'activity recognition']
A3 = ['machine learning', 'classification algorithm']
B = ['wildlife', 'animal']
C = ['unsupervised', 'clustering']

# the combinations I want to generate
combinations_AB = list(product(A1, A2, A3, B))
combinations_AC = list(product(A1, A2, A3, C))
long_combinations = list(product(A1, A2, A3, B, C))

search_strings = combinations_AB + combinations_AC + long_combinations