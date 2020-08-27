import gurobipy as gp 
from gurobipy import GRB 

# sets and indices 
products = ['p1', 'p2'] 
clusters = ['k1', 'k2'] 

# parameters 
cp, expected_profit = gp.multidict({
    ('k1', 'p1'): 2000,
    ('k1', 'p2'): 1000,
    ('k2', 'p1'): 3000,
    ('k2', 'p2'): 2000
}) 

cp, expected_cost = gp.multidict({ 
    ('k1', 'p1'): 200,
    ('k1', 'p2'): 100,
    ('k2', 'p1'): 300,
    ('k2', 'p2'): 200
})

clusters, number_customers = gp.multidict({('k1') : 5, ('k2') : 5 })
products, min_offers = gp.multidict({
    ('p1') : 2, ('p2') : 2}) 
R = 0.2 
budget = 200 

mt = gp.Model('Tactical') 
y = mt.addVars(cp, vtype = GRB.INTEGER, name = "allocate")
z = mt.addVar(vtype = GRB.CONTINUOUS, name = "budget_correction")


maxOffers_cons = mt.addConstrs((y.sum(k, '*') <= number_customers[k] for k in clusters), name = "maxOffers")
budget_con = mt.addConstr((y.prod(expected_cost) <= budget + z), name = 'budget') 
minOffers_cons = mt.addConstrs((gp.quicksum(y[k, j] for k in clusters) >= min_offers[j] for j in products), name = 'min_offers') 
ROI_con = mt.addConstr((y.prod(expected_profit) >= (1 + R) * y.prod(expected_cost)), name = 'ROI')

M = 10000 
mt.setObjective(y.prod(expected_profit) - M * z, GRB.MAXIMIZE)
mt.write('Tactical.lp')

mt.optimize() 

### Output Reports

# Optimal allocation of product offers to clusters

total_expected_profit = 0
total_expected_cost = 0

print("\nOptimal allocation of product offers to clusters.")
print("___________________________________________________")
for k,p in cp:
    if y[k,p].x > 1e-6:
        #print(y[k,p].varName, y[k,p].x)
        print(f"The number of customers in cluster {k} that gets an offer of product {p} is: {y[k,p].x}")
        total_expected_profit += expected_profit[k,p]*y[k,p].x
        total_expected_cost += expected_cost[k,p]*y[k,p].x

increased_budget = '${:,.2f}'.format(z.x)
print(f"\nThe increase correction in the campaign budget is {increased_budget}.")

# Financial reports

optimal_ROI = round(100*total_expected_profit/total_expected_cost,2)
min_ROI = round(100*(1+R),2)

money_expected_profit = '${:,.2f}'.format(total_expected_profit)
money_expected_cost = '${:,.2f}'.format(total_expected_cost)
money_budget = '${:,.2f}'.format(budget)

print(f"\nFinancial reports.")
print("___________________________________________________")
print(f"Optimal total expected profit is {money_expected_profit}.")
print(f"Optimal total expected cost is {money_expected_cost} with a budget of {money_budget} and an extra amount of {increased_budget}.")
print(f"Optimal ROI is {optimal_ROI}% with a minimum ROI of  {min_ROI}%.")
