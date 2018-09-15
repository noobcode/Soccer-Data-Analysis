import json
import numpy as np
import csv
import itertools

# lista di eventi di gioco 
events = json.load(open('../worldCup-final.json'))
grid = list(itertools.product(range(0,81,20), range(0,81,20)))
accurateID = {'id': 1801}

def is_event_in_cell(positions, cell):
    start_position = positions[0]
    start_x, start_y = start_position['x'], start_position['y']
    cell_x, cell_y = cell[0], cell[1]
    offset_x, offset_y = (start_x-cell_x), (start_y-cell_y)
    
    return offset_x <= 20 and (offset_x > 0 or (start_x == 0 and cell_x == 0))       and offset_y <= 20 and (offset_y > 0 or (start_y == 0 and cell_y == 0))


def opposing_team(team):
    if team == 'Croatia':
        return 'France'
    else:
        return 'Croatia'


# Inizializzazione
event_count= {}
teams = ['France', 'Croatia']
for team in teams:
    event_count[team]={}
    event_count[team]['total_events'] = 0
    event_count[team]['total_accurate_pass'] = 0
    event_count[team]['total_shots'] = 0
    event_count[team]['total_suffered_fouls'] = 0

# Riempimento
for event in events:
    
    team = event['teamId'] 
    event_count[team]['total_events'] += 1
    event_name = event['eventName']    
    key = None
    
    if event_name == 'Pass' and accurateID in event['tags']:
        event_count[team]['total_accurate_pass'] += 1
        key = 'accurate_pass_in_square'
        
    elif event_name == 'Shot':
        event_count[team]['total_shots'] += 1
        key = 'shots_in_square'
        
    # quando troviamo un fallo commesso (Foul) aumentiamo
    # il contatore dei falli subiti della squadra avversaria
    elif event_name == 'Foul':
        opposing = opposing_team(team)
        event_count[opposing]['total_suffered_fouls'] += 1
        key = 'suffered_fouls_in_square'
    
    for square in grid:
        if square not in event_count[team]:
            event_count[team][square] = {}
            event_count[team][square]['events_in_square'] = 0
            event_count[team][square]['accurate_pass_in_square'] = 0
            event_count[team][square]['shots_in_square'] = 0
            event_count[team][square]['suffered_fouls_in_square'] = 0
        
        if is_event_in_cell(event['positions'], square):
            event_count[team][square]['events_in_square'] += 1
            if key != None:
                if key == 'suffered_fouls_in_square':
                    event_count[opposing][square][key] += 1
                else:
                    event_count[team][square][key] += 1


header = ['nome_squadra',
          'numero_cella_x',
          'numero_cella_y',
          'frequenza_eventi',
          'frequenza_passaggi_accurati',
          'frequenza_tiri',
          'frequenza_falli_subiti']

with open("problema_3_a.csv", 'w+') as out_file:    
    writer = csv.writer(out_file)
    writer.writerow(header)
    
    for team in event_count.keys():
        statistics = event_count[team]
        tap = statistics['total_accurate_pass']
        te = statistics['total_events']
        ts = statistics['total_shots']
        tsf = statistics['total_suffered_fouls']

        for cell in grid:
            x = cell[0] / 20
            y = cell[1] / 20
            event_freq = statistics[cell]['events_in_square'] / float(te)
            acc_pass_freq = statistics[cell]['accurate_pass_in_square'] / float(tap)
            shots_freq = statistics[cell]['shots_in_square'] / float(ts)
            suff_fouls_freq = statistics[cell]['suffered_fouls_in_square'] / float(tsf)
            writer.writerow([team, x, y, event_freq, acc_pass_freq, shots_freq, suff_fouls_freq])
    

