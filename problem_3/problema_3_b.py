import csv
import numpy as np
import pandas as pd
from scipy.linalg import norm

def cosine_similarity(a, b):
    return float(np.dot(a, b)) / (norm(a)*norm(b))

grid = pd.read_csv('problema_3_a.csv')

header = ['tipo_griglia', 'similarity']
with open('problema_3_b.csv', 'w+') as out_file:    
    writer = csv.writer(out_file)
    writer.writerow(header)

    for i in range(3, 7):
        subgrid = grid.iloc[:, [0, i]]
        subgrid_france = subgrid[subgrid['nome_squadra'] == 'France']
        subgrid_croatia = subgrid[subgrid['nome_squadra'] == 'Croatia']

        values_france = subgrid_france.iloc[:, -1].values
        values_croatia = subgrid_croatia.iloc[:, -1].values
        
        writer.writerow([i-2, cosine_similarity(values_france, values_croatia)])    

