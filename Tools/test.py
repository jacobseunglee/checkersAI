import os

winCount = 0
rounds = 100

for i in range(rounds):
    os.system("python3 ./AI_Runner.py 8 8 3 l ../src/checkers-python/main.py ./Sample_AIs/Random_AI/main.py > tmp.txt")
    with open('tmp.txt') as f:
        for line in f:
            pass
        last_line = line

        print(last_line)

        stuff = last_line.split() # Doing it this way to avoid dumb whitespace errors

        if len(stuff) == 1:
            # Tie
            winCount += 1
        elif stuff[1] == '1':
            # Player 1 won
            winCount += 1
        else:
            # Player 2 won
            pass

percentage = winCount / rounds
print(winCount)
print(percentage)