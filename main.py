import random
from Network_Topology import getTopology
from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02

# ネットワークトポロジー1（ノード6リンク9）
graph = getTopology(topology_number=1)

# ネットワークトポロジー2（ノード6メッシュ型）
# graph = getTopology(topology_number=2)

# ネットワークトポロジー3（JPN12）
# graph = getTopology(topology_number=3)


# 実験回数、実験結果を保存する変数
number_of_running = 5
model = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02"]
results = {m:[] for m in model}

V = set(graph.nodes)
W_number = 30
W = {i+1 for i in range(W_number)}
C = {1, 2, 3, 4}
R = {}
R_number = 20

for i in range(number_of_running):
    print(f"実行{i+1}回目")
    for r in range(1,R_number+1):
        # ノードの中から2つをランダムで選択する
        [src, dist] = random.sample(list(V), 2)
        R[r] = (src, dist)

    for m in model:
        print(f"{m} is runnning...")
        runtime,w_max = eval(m)(graph=graph, R=R, W=W, C=C)
        results[m].append((runtime, w_max))
        print("done")


for m in model:
    print("------------------------")
    print(f"モデル：{m}")
    for runtime,w_max in results[m]:
        print(f"計算時間：{runtime} seconds / 波長の使用数：{w_max}")
    val = input("Push Entr to the next")