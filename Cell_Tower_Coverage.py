import gurobipy as gp 
from gurobipy import GRB 

budget = 20
regions, population = gp.multidict({
    0 : 523, 1 : 690, 2 : 420, 3 : 1010, 4 : 1200,
    5 : 850, 6 : 400, 7 : 1088, 8 : 950})
sites, coverage, cost = gp.multidict({
    0: [{0,1,5}, 4.2],
    1: [{0,7,8}, 6.1],
    2: [{2,3,4,6}, 5.2],
    3: [{2,5,6}, 5.5],
    4: [{0,2,6,7,8}, 4.8],
    5: [{3,4,8}, 9.2]
})

m = gp.Model("cell_tower")
build = m.addVars(len(sites), vtype = GRB.BINARY, name = "build")
is_covered = m.addVars(len(regions), vtype = GRB.BINARY, name = "is_covered")

m.addConstrs((gp.quicksum(build[i] for i in sites if j in coverage[i]) >= is_covered[j] for j in regions), name = "build2cover")
m.addConstr(build.prod(cost) <= budget, name = "budget")

m.setObjective(is_covered.prod(population), GRB.MAXIMIZE)

m.optimize()

for tower in build.keys():
    if (abs(build[tower].x) > 1e-6):
        print(f"\n Build a cell tower at location Tower {tower}.")

total_cost = 0

for tower in range(len(sites)):
    if (abs(build[tower].x) > 0.5):
        total_cost += cost[tower]*int(build[tower].x)


budget_consumption = round(100*total_cost/budget, 2)

print(f"\n The percentage of budget consumed associated to the cell towers build plan is: {budget_consumption} %")