import numpy as np
from tqdm import tqdm

File = "standards/examples/2.0/sample_2.0.las"
n,h=0,0
header = {}
with open(File,"r") as f:
    print("reading header")
    #parse header
    for line in tqdm(f, desc="reading header"):
            n +=1
            if line[0] == '~':
                print(line[1:])
                h+=1
                #fill dictionary
            else:
                print("process header")
                #something.append(line)
            if line[:2] == "~A":
                names= line.split()[1:]
                break
data = np.genfromtxt(File, skip_header=n, names=names)
