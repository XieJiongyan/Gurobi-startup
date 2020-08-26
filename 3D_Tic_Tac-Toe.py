import gurobipy as gp 
from gurobipy import GRB 

lines = []
size = 3

for i in range(size):
    for j in range(size):
        for k in range(size):
            if i == 0:
                lines.append(((0,j,k), (1,j,k), (2,j,k)))
            if j == 0:
                lines.append(((i,0,k), (i,1,k), (i,2,k)))
            if k == 0:
                lines.append(((i,j,0), (i,j,1), (i,j,2)))
            if i == 0 and j == 0:
                lines.append(((0,0,k), (1,1,k), (2,2,k)))
            if i == 0 and j == 2:
                lines.append(((0,2,k), (1,1,k), (2,0,k)))
            if i == 0 and k == 0:
                lines.append(((0,j,0), (1,j,1), (2,j,2)))
            if i == 0 and k == 2:
                lines.append(((0,j,2), (1,j,1), (2,j,0)))
            if j == 0 and k == 0:
                lines.append(((i,0,0), (i,1,1), (i,2,2)))
            if j == 0 and k == 2:
                lines.append(((i,0,2), (i,1,1), (i,2,0)))
lines.append(((0, 0, 0), (1, 1, 1), (2, 2, 2)))
lines.append(((2, 0, 0), (1, 1, 1), (0, 2, 2)))
lines.append(((0,2,0), (1,1,1), (2,0,2)))
lines.append(((0,0,2), (1,1,1), (2,2,0)))

print(lines)
model = gp.Model('Tic_Tac_Toe')
isX = model.addVars(size, size, size, vtype = GRB.BINARY, name = "isX")
isLine = model.addVars(lines, vtype = GRB.BINARY, name = "isLine")

x14 = model.addConstr(isX.sum() == 14)
for line in lines:
    model.addGenConstrIndicator(isLine[line], False, isX[line[0]] + isX[line[1]] + isX[line[2]] >= 1)
    model.addGenConstrIndicator(isLine[line], False, isX[line[0]] + isX[line[1]] + isX[line[2]] <= 2)

model.setObjective(isLine.sum(), GRB.MINIMIZE)
model.optimize()

import matplotlib.pyplot as plt 

fig, ax = plt.subplots(1, 3, figsize = (10, 5))
for i in range(3):
    ax[i].grid() 
    ax[i].set_xticks(range(4))
    ax[i].set_yticks(range(4))
    ax[i].tick_params(labelleft = False, labelbottom = False)

for cell in isX.keys():
    if isX[cell].x > 0.5:
        ax[cell[0]].add_patch(plt.Rectangle((cell[1], cell[2]), 1, 1))

plt.show()