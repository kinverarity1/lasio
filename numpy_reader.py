import numpy as np
from tqdm import tqdm

File = "standards/examples/2.0/sample_2.0.las"
headn=""
header = {}
with open(File,"r") as f:
    print("reading header")
    #parse header
    for line in tqdm(f, desc="reading header"):
            if line[0] == '~':
                if line[1] !="A":
                    headn=line[1:].strip()
                    header[headn]={}
                else:
                    names= line.split()[1:]
                    break
            else:
                if not line[0]=="#":
                    l=line.split()
                    header[headn][l[0]]=l[1:]
                #print("process header")
                #something.append(line)
data = np.genfromtxt(File, skip_header=n, names=names)
