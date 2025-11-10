import random
from tqdm import tqdm

from Network_Topology import getTopology
from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_03 import ILP_RCWA_03
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02
from ILP_RCWA_SLC_03 import ILP_RCWA_SLC_03
from Results_to_Excel import results_to_excel

# ネットワークトポロジー1（ノード6リンク9）
graph,topology_name = getTopology(topology_number=1)

# ネットワークトポロジー2（ノード6メッシュ型）
# graph,topology_name = getTopology(topology_number=2)

# ネットワークトポロジー3（JPN12）
# graph,topology_name = getTopology(topology_number=3)


# 実験回数
number_of_running = 50

# モデル
model = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03"]

# モデルごとの結果
results = {m:[] for m in model}

# モデルごとのruntime結果
results_runtime = {m:[] for m in model}

# モデルごとのwavelength結果
results_wavelength = {m:[] for m in model}

V = set(graph.nodes)
W_number = 20
W = {i+1 for i in range(W_number)}
C = {1, 2, 3, 4}
R = {}
R_number = 20

for i in tqdm(range(number_of_running)):
    for r in range(1,R_number+1):
        # ノードの中から2つをランダムで選択する
        [src, dist] = random.sample(list(V), 2)
        R[r] = (src, dist)

    for m in model:
        runtime,wavelength = eval(m)(graph=graph, R=R, W=W, C=C)
        results[m].append((runtime, wavelength))
        results_runtime[m].append(runtime)
        results_wavelength[m].append(wavelength)

# 平均の計算
for m in model:
    time_total = sum(results_runtime[m])
    time_average = time_total/len(results_runtime[m])
    w_total = sum(results_wavelength[m])
    w_average = w_total/len(results_wavelength[m])
    results[m].append((time_average,w_average))

results_to_excel(results=results, number_of_runnning=number_of_running, topology_name=topology_name, R_number=R_number)