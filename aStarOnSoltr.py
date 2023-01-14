from heapq import heapify, heappush, heappop

def calHr(state):
    ans=0
    for i in range(7):
        for j in range(7):
            if state[i][j]==1:
                H = abs(3-j)
                V = abs(3-i)
                ans+= 2**max(H,V)
    return ans

class Node:
    def __init__(self,st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]],prt=None,pCost=0):
        self.state = st
        self.parent = prt
        self.action = pCost
        self.pathCost = 0 # g
        self.value = calHr(self.state) # heuristic
        self.f = self.pathCost + self.value
    def __lt__(self, other):
        return self.value < other.value # min heap

goal = [[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]
def goalTest(state):
    return state==goal

def heuritic(i,j):
    H = abs(3-j)
    V = abs(3-i)
    return 2**max(H,V)

def getSuccessors(node):
    ans = []
    dx2 = [0,0,2,-2]
    dy2 = [-2,2,0,0]
    dx1 = [0,0,1,-1]
    dy1 = [-1,1,0,0]
    for i in range(7):
        for j in range(7):
            if node.state[i][j]==1:
                for k in range(4):
                    c2i = i+dy2[k]
                    c2j = j+dx2[k]
                    c1i = i+dy1[k]
                    c1j = j+dx1[k]
                    if(c2i<0 or c2i>=7 or c2j<0 or c2j>=7):
                        continue
                    if(node.state[c2i][c2j]==0):
                        stateCpy = [obj.copy() for obj in node.state]
                        hr = node.value
                        hr -= heuritic(i,j)
                        hr -= heuritic(c1i,c1j)
                        hr += heuritic(c2i,c2j)
                        child = Node(stateCpy,node,node.pathCost+1)
                        child.value = hr
                        child.f = child.pathCost + child.value
                        child.state[c2i][c2j]=1
                        child.state[c1i][c1j]=0
                        child.state[i][j]=0
                        child.action = [[i,j],[c2i,c2j]]
                        ans.append(child)
    return ans


def displayBoard(state):
    for row in state:
        print(row)

def aStar():
    start_node = Node()
    frontier = [] # keep nodes
    heapify(frontier)
    explored = [] # keep states which are explored

    heappush(frontier,start_node)
    while True:
        if len(frontier)==0:
            return None
        curr = heappop(frontier)
        displayBoard(curr.state)
        print()
        if curr.state in explored:
            continue
        if goalTest(curr.state) == True:
            return curr
        children = getSuccessors(curr)
        for child in children:
            if (child.state in explored) == False:
                heappush(frontier,child)
        explored.append(curr.state)

ans = aStar()
print(ans)

