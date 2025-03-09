# Import libraries
!pip install pulp
import pulp

# Define problem: Minimize transportation costs
problem = pulp.LpProblem("Supply_Chain_Optimization", pulp.LpMinimize)

# Warehouses (supply) and Retailers (demand)
warehouses = ['Warehouse_1', 'Warehouse_2']
retailers = ['Retailer_A', 'Retailer_B', 'Retailer_C']

# Supply and Demand (units)
supply = {'Warehouse_1': 1000, 'Warehouse_2': 1500}
demand = {'Retailer_A': 800, 'Retailer_B': 900, 'Retailer_C': 800}

# Transportation costs per unit
costs = {
    ('Warehouse_1', 'Retailer_A'): 2.5,
    ('Warehouse_1', 'Retailer_B'): 3.0,
    ('Warehouse_1', 'Retailer_C'): 4.0,
    ('Warehouse_2', 'Retailer_A'): 3.5,
    ('Warehouse_2', 'Retailer_B'): 2.8,
    ('Warehouse_2', 'Retailer_C'): 3.2,
}

# Decision variables
routes = [(w, r) for w in warehouses for r in retailers]
x = pulp.LpVariable.dicts("Route", routes, lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum([x[(w, r)] * costs[(w, r)] for (w, r) in routes])

# Constraints
for w in warehouses:
    problem += pulp.lpSum([x[(w, r)] for r in retailers]) <= supply[w]

for r in retailers:
    problem += pulp.lpSum([x[(w, r)] for w in warehouses]) >= demand[r]

# Solve
problem.solve()

# Print results
print("Optimal Transportation Plan:")
for (w, r) in routes:
    if x[(w, r)].varValue > 0:
        print(f"{w} -> {r}: {x[(w, r)].varValue:.0f} units")

print(f"\nTotal Cost: ${pulp.value(problem.objective):.2f}")
