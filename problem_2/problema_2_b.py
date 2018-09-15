import csv
import json
import numpy as np

path_to_data = '../'
output_file = '../problema_2_b.csv'

players = json.load(open(path_to_data + 'players.json'))
events = json.load(open(path_to_data + 'worldCup-final.json'))

tackle_won_tag_id = 703

players_mte_2_tackles = []

for pl in players:
    
    tackles_count = 0
    tackles_won = 0
    
    for ev in events:
        if ev['playerId']==pl['playerId'] and ev['subEventName']=='Ground defending duel':
            
            tackles_count = tackles_count + 1
            tags = ev['tags']
            for t in tags:
                if t['id']==tackle_won_tag_id:
                    tackles_won = tackles_won + 1

    if tackles_count >= 2:
        players_mte_2_tackles.append((pl['playerId'], pl['name'], tackles_won))

_, _, tws = zip(*players_mte_2_tackles)
players_output = [(pid, name, tw) for (pid, name, tw) in players_mte_2_tackles 
                  if tw >= np.percentile(tws, 75)]


with open(output_file, 'w') as out:
    wr = csv.writer(out, delimiter=',')
    wr.writerow(['identificativo_calciatore', 'nome_calciatore', 'tackle_vinti'])
    
    for (pid, pname, tw) in players_output:
        wr.writerow(list((pid, pname.encode('utf8'), tw)))

