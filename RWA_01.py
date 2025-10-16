from gurobipy import Model,GRB
from Routing import routing
from welch_powell import WP
import networkx as nx
import matplotlib.pyplot as plt
from odd_cycles import getCycles

# ネットワークを模した無向グラフG=(V,E)
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
G.add_edges_from([(1,12), (1,27), (2,3), (2,13), (2,28), (3,4), (3,14), (4,5), (4,17), (5,6), (5,21), (6,7), (6,16), (7,8), (8,9), (8,23), (9,10),
     (10,11), (10,15), (11,24), (12,13), (12,15), (12,26), (14,15), (14,16), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23),
     (24,25), (25,26), (27,28)])
V =  set(G.nodes)  # ノード集合
E = set(G.edges)    # 無向リンク集合


E_outgoing = {v:set() for v in V}   # N^+(v)
E_incoming = {v:set() for v in V}   # N^-(v)
E_directed = set()  # 有向リンク集合
for u,v in E:
    E_outgoing[u].add((u,v))
    E_outgoing[v].add((v,u))
    E_incoming[u].add((v,u))
    E_incoming[v].add((u,v))
    E_directed |= {(u,v),(v,u)}
    
# for v in V:
#     print(f"{v}から出るリンク集合：{E_outgoing[v]}")
#     print(f"{v}へ入るリンク集合：{E_incoming[v]}")

# R = [(1,9), (2,5), (3,16), (8,22), (21,10), (9,5), (6,1), (4,28), (19,25)]
R = {1:(1,9), 2:(2,5), 3:(3,16), 4:(8,22), 5:(21,10), 6:(9,5), 7:(6,1), 8:(4,28), 9:(23,25)}    # リクエスト集合

# # routing
path, w_use = routing(R, V, E_directed, E_outgoing, E_incoming)

# リクエストをノードとした隣接グラフG-R=(V_R,E_R)
G_R = nx.Graph()
G_R.add_nodes_from(list(R.keys()))
W = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
colorList = {1:"red", 2:"blue", 3:"yellow", 4:"green", 5:"pink"}

for r1 in R:
    p1 = path[r1]
    for r2 in R:
        if r1 < r2:
            p2 = path[r2]
            if not p1.isdisjoint(p2):
                G_R.add_edge(r1,r2)


# for r in R:
#     print(path[r])
# print('--- リンクを共有するリクエスト ---')
# print(list(G_R.edges))

w_alloc, w_wp = WP(G_R,colors=W.copy())
nx.draw(G_R, node_color = [colorList[wavelength] for wavelength in list(w_alloc.values())],with_labels=True)
plt.show()

loop = 0
if w_wp > w_use:
    if w_use < 3:

        cycleList = []
        oddCycleList = []
        pares = []
        getCycles(G_R,cycleList,1,-1)
        for cycle in cycleList:
            if len(cycle) > 3 and len(cycle)%2 == 1:    oddCycleList.append(cycle)
        while len(oddCycleList) > 0:
            # 奇閉路に使用される回数を記録する
            freqency = {r:0 for r in R}
            for oddCycle in oddCycleList:
                for v in oddCycle:
                    freqency[v] += 1
            # 大きさが最大の閉路を見つける
            largestCycle = oddCycleList[0]
            for oddCycle in oddCycleList:
                if len(largestCycle) < len(oddCycle):   largestCycle = oddCycle
            # 次元数が最小のノードを見つける
            least = largestCycle[0]
            for v in largestCycle:
                if G_R.degree[least] > G_R.degree[v]: least = v
            # 閉路内の辺を1本カッティング
            largest = -1
            frq = 0
            for v in list(G_R.adj[least].keys()):
                if v in largestCycle and frq < freqency[v]:
                    largest = v
                    frq = freqency[largest]
            G_R.remove_edge(least, largest)
            pares.append((least, largest))
            oddCycles_remove = [] # (least, largest)の辺を持つ奇閉路をまとめて消す
            for oddCycle in oddCycleList:
                if least in oddCycle and largest in oddCycle:
                    oddCycles_remove.append(oddCycle)
            for remove in oddCycles_remove:
                oddCycleList.remove(remove)
        # RWAを更新して実行
        path, w_use = routing(R, V, E_directed, E_outgoing, E_incoming,pares=pares)
        w_alloc, w_wp = WP(G_R, colors=W.copy())
    else:   pass
else:   pass

print(f"削除するリンク：{pares}")
for r in R:
    print(f"リクエスト{r}")
    print(f"パス：{path[r]}")
    print(f"使用する波長：{w_alloc[r]}")
    print("----------------------------")

nx.draw(G_R, node_color = [colorList[wavelength] for wavelength in list(w_alloc.values())],with_labels=True)
plt.show()