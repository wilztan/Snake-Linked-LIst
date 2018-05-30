from time import sleep

print('Please provide input in 20 seconds! (Hit Ctrl-C to start)')
try:
    for i in range(0,10):
        sleep(1) # could use a backward counter to be preeety :)
    print('No input is given.')
except KeyboardInterrupt:
    raw_input('Input x:')
    print('You, you! You know something.')
