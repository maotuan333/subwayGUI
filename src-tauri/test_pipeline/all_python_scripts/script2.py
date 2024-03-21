with open(".\\step1.docx",'r') as f:
    l=f.readline().split()
with open(".\\step2.csv",'w') as f:
    f.write(','.join(l)+"\n"+"even,more,processing")
