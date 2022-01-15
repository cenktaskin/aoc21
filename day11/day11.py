import numpy as np

input_file = "input.txt"
raw_input = np.genfromtxt(input_file, dtype=str)
raw_input = np.array([[ch for ch in x] for x in raw_input],dtype=int)

def get_neighbours(mat,loc):
    return slice(max(0,loc[0]-1),min(mat.shape[0],loc[0]+2)),slice(max(0,loc[1]-1),min(mat.shape[1],loc[1]+2))

    #implemenet from matrix to neighbours

def step(octopus_field, goal):
    i=0
    #print(f"Starting field")
    #print(octopus_field)
    flash_tracker = np.zeros_like(octopus_field)
    octopus_field += 1
    #print("after increase")
    #print(octopus_field)
    flashing_octopus = octopus_field > 9
    while np.any(flashing_octopus):
        i+=1
        # implement a parallel table where you count flashed octopuses every step, so no double-flashing!
        row,col = np.where(flashing_octopus)
        loc = np.argwhere(flashing_octopus)[0]
        x,y = get_neighbours(octopus_field,loc)
        #print(f"flashing {loc}")
        flash_tracker[tuple(loc)] += 1
        octopus_field[x,y] += 1
        #print(flash_tracker==1)
        octopus_field[flash_tracker==1]=0
        #print(octopus_field)
        flashing_octopus = octopus_field > 9
    goal += np.sum(flash_tracker)
    return octopus_field, goal

inp = raw_input
count = 0
i = 0
while True:
    #cond = i == 100 #part1
    cond = np.all(inp==0) #part2
    if cond:
        break
    print(f"step {i+1}")
    inp,count = step(inp,count)
    print(f"{count} flashes")
    print(f"{inp==0} octopus has flashed")
    i+=1



