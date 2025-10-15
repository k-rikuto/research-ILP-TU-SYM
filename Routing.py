from gurobipy import Model,GRB,quicksum

def routing(R:dict, V:set, E:set, E_outgoing:dict, E_incoming:dict):
    model = Model("routing")

    x = {}
    for r in R:
        for e in E:
            x[r,e] = model.addVar(vtype=GRB.BINARY, name=f"request{r}, edge{e}")
    
    w_max = model.addVar(vtype=GRB.INTEGER, name="maximum of wavelength")
    model.update()

    for r in R:
        src,dest = R[r]
        model.addConstr(quicksum(x[r,e] for e in E_incoming[src])-quicksum(x[r,e] for e in E_outgoing[src])==-1)
        model.addConstr(quicksum(x[r,e] for e in E_incoming[dest])-quicksum(x[r,e] for e in E_outgoing[dest])==1)
        for v in V-{src,dest}:
            model.addConstr(quicksum(x[r,e] for e in E_incoming[v])-quicksum(x[r,e] for e in E_outgoing[v])==0)
    
    for e in E:
        model.addConstr(quicksum(x[r,e] for r in R)<=w_max)
    
    model.setObjective(w_max, GRB.MINIMIZE)
    model.optimize()

    path = {r:set() for r in R}
    EPS = 1.e-6
    for r,e in x:
        v1,v2 = e
        if x[r,e].X>EPS:
            if v1 > v2: path[r].add((v2,v1))
            else:   path[r].add(e)

    return path, w_max.X