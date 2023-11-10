import os

winCount = 0
rounds = 1000
stop = False
for i in range(rounds):
    os.system("python3 ./AI_Runner.py 8 8 3 l ../main.py ./Sample_AIs/Random_AI/main.py > new.txt")
    f = open("new.txt", "r")
    for line in f:
        if "crashed" in line:
            stop = True
        if stop:
            break
    if stop:
        break
    last_line = line

    print(last_line)
    stuff = last_line.split() # Doing it this way to avoid dumb whitespace errors

    if len(stuff) == 1:
        # Tie
        winCount += 1
    elif stuff[1] == '1':
        # Player 1 won
        pass
    else:
        # Player 2 won
        winCount += 1
    print(f"current win ratio: {winCount/(i+1)}")
f.close()
percentage = winCount / (i+1)
print(winCount)
print(percentage)
