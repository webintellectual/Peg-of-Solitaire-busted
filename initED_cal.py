state = [[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]]

ans = 0
for i in range(7):
    for j in range(7):
        if state[i][j]==1:
            H = abs(3-j)
            V = abs(3-i)
            ans += 2**max(H,V)

print("ans: ", ans)