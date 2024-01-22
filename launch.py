import subprocess

num_matches = 5
black_wins = 0
white_wins = 0

for _ in range(num_matches):
    
    result = subprocess.run(['python3', 'withoutgraphic.py'], capture_output=True, text=True)
    output = result.stdout.strip()
    
    # Check the output to determine the winner
    if "Black wins!" in output:
        black_wins += 1
    elif "White wins!" in output:
        white_wins += 1

print(f"Black wins: {black_wins} times")
print(f"White wins: {white_wins} times")
