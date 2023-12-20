l = '/Users/akadilkalimoldayev/Downloads/buy_pv_0512_0948_7432275.pdf'

for ind in range(len(l)-1, -1, -1):
    if l[ind] == "/":
        break

print(l[ind+1:])

