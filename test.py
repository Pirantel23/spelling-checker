f = open('data.txt', 'r')
sum = 0
for line in f.read().split('\n'):
    sum+=float(line.split()[-1])
print(sum)