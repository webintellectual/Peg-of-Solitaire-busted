import time

"""
Author : Akshay Rajput
© Anyone must take permission form me and mention my social handles in 
the references/attributes before using this code in their work or project.
Linkedin: https://www.linkedin.com/in/akshay-189a48200/
Twitter: https://twitter.com/notifications
Medium: https://medium.com/@warriorak77
GitHub: https://github.com/webintellectual
Website: https://akshaysworklife.bio.link/
"""

class Node:
    def __init__(self,st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]],prt=None,pCost=0):
        self.state = st
        self.parent = prt
        self.action = None
        self.pathCost = pCost # g
    def __lt__(self, other):
        return self.pathCost < other.pathCost # min heap

goal = [[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]
def goalTest(state):
    return state==goal

Total_nodes_expanded = 0
def getSuccessors(node):
    ans = []

    # Good order of directions # NSEW
    dx2 = [0,0,2,-2]
    dy2 = [-2,2,0,0]
    dx1 = [0,0,1,-1]
    dy1 = [-1,1,0,0]
    # y-> i, x -> j

    # Bad order of direction #WESN
    # dx2 = [-2,2,0,0]
    # dy2 = [0,0,2,-2]
    # dx1 = [-1,1,0,0]
    # dy1 = [0,0,1,-1]

    for i in range(7):
        for j in range(7):
            if node.state[i][j]==1:
                for k in range(4):
                    # print("i,j: ",i,j)
                    c2i = i+dy2[k]
                    c2j = j+dx2[k]
                    c1i = i+dy1[k]
                    c1j = j+dx1[k]
                    # print("c1i, c1j", c1i,c1j)
                    # print("c2i, c2j: ",c2i,c2j)
                    if(c2i<0 or c2i>=7 or c2j<0 or c2j>=7):
                        continue
                    if(node.state[c1i][c1j]==0):
                        continue
                    if(node.state[c2i][c2j]==0):
                        stateCpy = [obj.copy() for obj in node.state]
                        child = Node(stateCpy,node,node.pathCost+1)
                        child.state[c2i][c2j]=1
                        child.state[c1i][c1j]=0
                        child.state[i][j]=0
                        child.action = [[i,j],[c2i,c2j]]
                        ans.append(child)
                        global Total_nodes_expanded
                        Total_nodes_expanded +=1
    return ans


def displayBoard(state):
    for row in state:
        print(row)

def BestFS():
    start_node = Node()
    frontier = [] # keep nodes # we can use list directly as a heap in python. append() and pop() for push and pop
    explored = [] # keep states which are explored

    frontier.append(start_node)
    while True:
        # print("flag")
        if len(frontier)==0:
            return None
        curr = frontier.pop()

        displayBoard(curr.state)
        print("Path cost: ", curr.pathCost)
        print()

        if curr.state in explored:
            continue
        if goalTest(curr.state) == True:
            print("Search ended")
            print("Total nodes explored: ", len(explored)) 
            return curr
        children = getSuccessors(curr)
        for child in children:
            if (child.state in explored) == False:
                frontier.append(child)
        explored.append(curr.state)

def allActions(goalNode):
    ans = []
    while goalNode.parent != None:
        ans.append(goalNode.action)
        goalNode = goalNode.parent
    ans.reverse()
    return ans

print("Search started")
start_time = time.time()
ans = BestFS()
end_time = time.time()
elapsed_time = end_time - start_time
print("Total nodes expanded: ",Total_nodes_expanded)
print("Time taken: ",elapsed_time)
print()
displayBoard(ans.state)

print()
print("Moves: ")
moves = allActions(ans)
for move in moves:
    print(move)
