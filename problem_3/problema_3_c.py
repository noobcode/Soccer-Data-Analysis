import csv
import pandas as pd

grid = pd.read_csv('problema_3_a.csv')
grid_croatia = grid[grid['nome_squadra'] == 'Croatia']
grid_france = grid[grid['nome_squadra'] == 'France']

header = ['tipo_griglia',
          'numero_cella_x',
          'numero_cella_y',
          'squadra_dominante',
          'differenza_di_frequenza']

with open('problema_3_c.csv', 'w+') as out_file:    
    writer = csv.writer(out_file)
    writer.writerow(header)
    
    for i in range(len(grid_croatia)):
        row_croatia = grid_croatia.iloc[i].values
        row_france = grid_france.iloc[i].values

        for j in range(3, len(row_croatia)):
            freq_croatia = row_croatia[j]
            freq_france = row_france[j]
            if freq_croatia > freq_france:
                winner = 'Croatia'
            else: 
                winner = 'France'
            diff = abs(freq_croatia - freq_france)

            grid_type = j - 2
            cell_x = row_croatia[1]
            cell_y = row_croatia[2]

            row_to_write = [grid_type, cell_x, cell_y, winner, diff]
            writer.writerow(row_to_write)
        

