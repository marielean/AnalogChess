from concurrent.futures import ProcessPoolExecutor
from withoutgraphic import run_match

# Configurable parameters
max_threads = 10 # questo deve essere il numero di virtual cores del server 
num_matches_for_config = 5 # qua bisognerebbe farne 50 almeno

# Commento generale: penso che oltre profondità 3 si farà fatica a meno che non abbiate a disposizione tempo illimitato di esecuzione sul server
# In tal caso si potrebbe tentare di fare anche 4 (forse) lasciandolo andare circa una settimana. Il requisito è che koka non termini il processo
# dopo un tot.
configurations = [
    # Random-Random for test -> it should be 50% - 50%
    ['Random', 'Random', 1, 1, 1],
    # Random-AlphaBeta -> it should be approx 100% - 0%
    ['AlphaBeta', 'Random', 1, 1, 1], # depth_black non serve davvero
    ['AlphaBeta', 'Random', 2, 1, 1],
    # AlphaBeta-AlphaBeta con uguale profondità -> it should be approx 50% - 50% e si può osservare la dipendenza del tempo di esecuzione dalla profondità
    ['AlphaBeta', 'AlphaBeta', 1, 1, 1],
    ['AlphaBeta', 'AlphaBeta', 2, 2, 1],
    ['AlphaBeta', 'AlphaBeta', 3, 3, 1], # (circa 20 min di esecuzione a match -> 17h per 50 esecuzioni)
    # AlphaBeta-AlphaBeta con varie granularità (uguale profondità) -> L'idea è vedere la dipendenza del tempo di esecuzione dalla granularità
    ['AlphaBeta', 'AlphaBeta', 2, 2, 2],
    ['AlphaBeta', 'AlphaBeta', 2, 2, 3],
    ['AlphaBeta', 'AlphaBeta', 2, 2, 4],
    ['AlphaBeta', 'AlphaBeta', 2, 2, 5],
    ['AlphaBeta', 'AlphaBeta', 2, 2, 10],
    # AlphaBeta-AlphaBeta con diverse profondità -> È il test più interessante e mostra come aumentando la profondità aumenti "l'intelligenza"
    ['AlphaBeta', 'AlphaBeta', 2, 1, 4],
    ['AlphaBeta', 'AlphaBeta', 3, 1, 4],
    ['AlphaBeta', 'AlphaBeta', 3, 2, 4],
    ['AlphaBeta', 'AlphaBeta', 3, 3, 4], # qua si dovrebbe riottenere un 50% - 50% 
    # La prova con MinMax è interessante per vedere quanto si guadagna in termini di tempo di esecuzione con i tagli alpha-beta
    ['MinMax', 'MinMax', 2, 2, 4], # La scelta dei parametri è per non richiedere troppo tempo ma si possono aggiungere altri test
]


# Statistics
winner_ratio = []
mean_time = []
mean_number_of_turns = []

# for _ in range(num_matches):
    
#     result = subprocess.run(['python3', 'withoutgraphic.py'], capture_output=True, text=True)
#     output = result.stdout.strip()
    
#     # Check the output to determine the winner
#     if "Black wins!" in output:
#         black_wins += 1
#     elif "White wins!" in output:
#         white_wins += 1

# Stampa su file .csv l'intestazione
with open('results.csv', 'w') as f:
    print('white_algorithm; black_algorithm; white_depth; black_depth; granularity; white_wins [%]; mean_match_time [s]; mean_turns_number', file=f)

for configuration in configurations:
    black_wins = 0
    white_wins = 0
    execution_times = []
    number_of_turns = []
    threads = []

    print("Running match with configuration: ", configuration[0], configuration[1], configuration[2], configuration[3], configuration[4])

    print('Progress: ', end='')
    with ProcessPoolExecutor(max_workers=max_threads) as executor:
        threads = [executor.submit(run_match, configuration[0], configuration[1], configuration[2], configuration[3], configuration[4]) for _ in range(num_matches_for_config)]

    print("") # A capo

    for thread in threads:
        result = thread.result()
        white_wins += 1 if result[0] else 0
        execution_times.append(result[1])
        number_of_turns.append(result[2])
    black_wins = num_matches_for_config - white_wins

    mean_time.append(sum(execution_times) / len(execution_times))
    mean_number_of_turns.append(sum(number_of_turns) / len(number_of_turns))

    # Stampa su file .csv le statistiche di questa configurazione
    with open('results.csv', 'a') as f:
        print('Results:\n', '\twhite_wins', white_wins/num_matches_for_config*100, '%', '\n\tMean_execution_time: ', mean_time[-1], 's', '\n\tMean_number_of_turns: ', mean_number_of_turns[-1],'\n')
        print(configuration[0], configuration[1], configuration[2], configuration[3], configuration[4], white_wins/num_matches_for_config*100, mean_time[-1], mean_number_of_turns[-1], sep='; ', file=f)
