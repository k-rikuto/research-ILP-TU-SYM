from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


LIMITE_OF_NODE = 100
visited = [False]*LIMITE_OF_NODE
history = []
def getCycles(graph:nx.Graph, cycleList:list,v:int, former:int):
    global visited
    global history

    # print(f"過去の経路：{history}")
    # 閉路を検知
    if visited[v]:
        cycle = [v]
        for u in reversed(history):
           if u==v: break
           cycle.append(u)
        cycle.sort()
        # print(f"閉路：{cycle}")
        same = False
        for cycle2 in cycleList:
            if cycle2==cycle:   same = True
        if not same:    cycleList.append(cycle)
    # 検知できなかったとき
    else:
        # 訪れた場所を記録
        visited[v] = True
        history.append(v)
        # 次の点を探索
        for u in list(graph.adj[v].keys()):
            if former==u: continue    # 後戻りのノードをスキップ
            getCycles(graph,cycleList,u,v)
        # 探索が終了
        history = history[:-1]
        visited[v] = False


# 動作確認
# G = nx.wheel_graph(5)
# cycleList= []
# getCycles(G,cycleList,0,-1)

# print(cycleList)
# nx.draw_networkx(G)
# plt.show()