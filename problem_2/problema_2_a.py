import json
import numpy as np
import csv

# lista di eventi di gioco 
events = json.load(open('../worldCup-final.json'))
players = json.load(open('../players.json'))

accurateID = {'id': 1801}

event_count= {}

# Accuratezza media dei passaggi
# Per ogni squadra, memorizza il numero di passaggi accurati e il numero totale di passaggi (per ogni giocatore)

for event in events:
    team = event['teamId']
    
    # considera soltanto gli eventi 'Pass'
    event_type = event['eventName']
    if event_type != 'Pass':
        continue
    
    # controlla se il passaggio e' accurato
    is_accurate = accurateID in event['tags']
    
    player_id = event['playerId']
    
    if team not in event_count:
        event_count[team]={}
        
    if player_id not in event_count[team]:
        event_count[team][player_id] = {}
        event_count[team][player_id]['total_pass'] = 0
        event_count[team][player_id]['accurate_pass'] = 0
    
    event_count[team][player_id]['total_pass'] += 1
    
    if is_accurate:
        event_count[team][player_id]['accurate_pass'] += 1


teams = event_count.keys()

def compute_mean_and_std(passes, team_name):
    accuracies = [ float(v['accurate_pass']) / v['total_pass'] for v in passes[team_name].values() ]
    return [team_name, np.mean(accuracies), np.std(accuracies)]

with open("problema_2_a.csv", 'w+') as out_file:    
    writer = csv.writer(out_file)
    header = ['nome_squadra',
              'accuratezza_media_dei_passaggi',
              'standard_deviation_accuratezza_media_dei_passaggi']
    writer.writerow(header)
    for t in teams:
        row = compute_mean_and_std(event_count, t)
        writer.writerow(row)






