with open(".\\step0.txt",'r') as f:
    l=f.readline().split('"')[1]
with open(".\\step1.txt",'w') as f:
    f.write(l)
