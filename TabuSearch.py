import networkx as nx

# 入力：G-Rグラフ、w_alloc：割り当てられた波長、w_use：最大波長数の下限、
def TabuSearch(graph:nx.Graph, w_alloc:dict[int,int], w_use:int, T:int, omega:int):
    # タブーリストHと反復回数IterCountを初期化
    H = []
    IterCount = 0
    for r in set([r for r in list(w_alloc.keys()) if w_alloc[r] > w_use]):
        pass