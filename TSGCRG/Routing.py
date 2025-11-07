from gurobipy import Model,GRB,quicksum

# pares: リンクを共有しないノードのペア(v,u)の集合
def routing(R:dict, V:set, E:set, E_outgoing:dict, E_incoming:dict, pares:list[tuple]=None):
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
        v,u = e
        e_reverse = (u,v)
        if v < u:
            model.addConstr(quicksum(x[r,e] for r in R)+quicksum(x[r,e_reverse] for r in R)<=w_max)
    
    # リクエストr1とリクエストr2がリンクを共有しないようにする制約
    if pares is not None:
        print("制約あり")
        for r1,r2 in pares:
            for e in E:
                v,u = e
                e_reverse = (u,v)
                if v < u:
                    model.addConstr(x[r1,e]+x[r2,e]+x[r1,e_reverse]+x[r2,e_reverse]<=1)
    
    model.setObjective(w_max, GRB.MINIMIZE)
    model.optimize()

    path = {r:set() for r in R}
    EPS = 1.e-6
    for r,e in x:
        v,u = e
        if x[r,e].X>EPS:
            if v > u:   path[r].add((u,v))
            else:   path[r].add(e)

    return path, w_max.X