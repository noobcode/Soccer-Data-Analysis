import json
import pandas as pd

# lista di eventi di gioco fornita in formato json
players = json.load(open('../players.json'))
events = json.load(open('../worldCup-final.json'))

df_players = pd.DataFrame(players)
df_players = df_players.set_index('playerId')

df_events = pd.DataFrame(events)

# preprocessing
def transform_pos(x):
	# assumiamo che la posizione finale dell'evento manca, allora
	# e' uguale alla posizione iniziale.
    if len(x) < 2:
        x.append(x[0])
    return x

df_events['positions'] = df_events['positions'].apply(transform_pos)
df_events['x_start'] = [p[0]['x'] for p in df_events['positions']]
df_events['y_start'] = [p[0]['y'] for p in df_events['positions']]
df_events['x_end'] = [p[1]['x'] for p in df_events['positions']]
df_events['y_end'] = [p[1]['y'] for p in df_events['positions']]

# rimuovere il signor arbitro (playerId = 0)
df_events = df_events[df_events['playerId'] != 0] 

# (i) Calcolo del tempo medio tra due eventi, e del tempo totale giocato per giocatore e match period
# il risultato e' un dataframe che verra' riaggregato per giocatore mediando sui risultati dei match period
df_player_period = list(df_events.groupby(['playerId', 'matchPeriod']))

avgOverPeriod = [ {'identificativo_calciatore': player[0][0],
				    'matchPeriod': player[0][1],
                    'tempo_medio_tra_eventi': player[1]['eventSec'].sort_values(ascending=True).diff().mean()} 
				for player in df_player_period]

totTimeDf = [ {'identificativo_calciatore': player[0][0],
				    'matchPeriod': player[0][1],
                    'totTime': (player[1]['eventSec'].max() - player[1]['eventSec'].min())} 
				for player in df_player_period]

df_avg_between_events = pd.DataFrame(avgOverPeriod).groupby('identificativo_calciatore').mean()
df_totTime = pd.DataFrame(totTimeDf).groupby('identificativo_calciatore').sum()

# creo filtro per eliminare dal calcolo della media i giocatori che hanno giocato per meno di 45 min (45*60s)
mask = df_totTime['totTime'] <= 2700
nonConsiderati = list(df_totTime[mask].index)

df_pos_media = pd.DataFrame(df_events.playerId)
df_pos_media = df_pos_media[~df_pos_media['playerId'].isin(nonConsiderati)]

#calcolo posizione media per giocatori che hanno giocato piu di 45 min
df_pos_media['posizione_media_x'] = (df_events['x_start'] + df_events['x_end']) / 2
df_pos_media['posizione_media_y'] = (df_events['y_start'] + df_events['y_end']) / 2
df_pos_media.head()

data_grouped = df_pos_media.groupby('playerId')
posizione_media = data_grouped.mean()
df_posizione_media = posizione_media[['posizione_media_x','posizione_media_y']]

#calcolo distanza quadratica media
positions = ['x_start', 'x_end', 'y_start', 'y_end']
variances = df_events.groupby('playerId')[positions].var(ddof=0).sum(axis=1)
df_quad = pd.DataFrame(variances, columns=['distanza_quadratica_media'])

df_teams = df_events[['playerId','teamId']].drop_duplicates().set_index('playerId')

# concateno single dataframes and print output
df_output = pd.concat([df_players, df_teams, df_posizione_media, df_quad, df_avg_between_events], axis=1)
df_output.reset_index(level=0,inplace=True)
df_output.rename(index=str, columns={"index":"identificativo_calciatore",
									 "name": "nome_calciatore", 
								     "teamId": "squadra_calciatore"}, inplace=True)
df_output.to_csv('problema_1.csv', index=False)

