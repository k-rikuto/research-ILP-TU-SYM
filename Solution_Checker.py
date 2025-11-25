import random as rd
from tqdm import tqdm

from Network_Topology import get_topology
from ILP_RCWA_01 import ILP_RCWA_01
from ILP_RCWA_02 import ILP_RCWA_02
from ILP_RCWA_03 import ILP_RCWA_03
from ILP_RCWA_SLC_01 import ILP_RCWA_SLC_01
from ILP_RCWA_SLC_02 import ILP_RCWA_SLC_02
from ILP_RCWA_SLC_03 import ILP_RCWA_SLC_03
from ILP_RWA_01 import ILP_RWA_01
from ILP_RWA_02 import ILP_RWA_02
from ILP_RWA_03 import ILP_RWA_03
from Results_to_Excel import results_to_excel

# RCWAモデル
MODEL_RCWA = ["ILP_RCWA_01", "ILP_RCWA_02", "ILP_RCWA_03", "ILP_RCWA_SLC_01", "ILP_RCWA_SLC_02", "ILP_RCWA_SLC_03"]

# RWAモデル
MODEL_RWA = ["ILP_RWA_01", "ILP_RWA_02", "ILP_RWA_03"]


'''
関数名：check_solution
<概要>
モデル
'''
def check_solution():
    # 変更場所
    R_number = 80          # リクエストの数
    model = MODEL_RCWA[0]       # 検証で扱うモデル

    # 実験に使用するネットワークトポロジーを選択する
    # ネットワークトポロジー1（ノード6リンク9）
    # graph,topology_name = get_topology(topology_number=1)

    # ネットワークトポロジー2（ノード6メッシュ型）
    # graph,topology_name = get_topology(topology_number=2)

    # ネットワークトポロジー3（JPN12）
    graph,topology_name = get_topology(topology_number=3)

    # 実験環境の表示
    print('<実験情報>')
    print(f"ネットワークトポロジー名：{topology_name}")
    print(f"リクエストの数：{R_number}")
    print(f"モデルの名前：{model}")

    # 実行確認
    # 変更が反映されてない状態で実行してしまうのを防ぐために確認する
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y":  pass
    else:   return

    # ノード集合からリクエストを生成するため
    V = set(graph.nodes)

    # 波長
    W_number = 30
    W = {i+1 for i in range(W_number)}

    # コアの集合
    C = {1, 2, 3, 4}

    # リクエストの集合
    R = {}
    for r in range(1,R_number+1):
        # ノードリストの中から2つをランダムで選択する
        [src, dist] = rd.sample(list(V), 2)
        R[r] = (src, dist)
    

    # モデルの実行
    if model in MODEL_RCWA:
        path,w_alloc = eval(model)(graph=graph, R=R, W=W, C=C, getPath=True)
    else:
        path,w_alloc = eval(model)(graph=graph, R=R, W=W, getPath=True)

    ## リクエスト1~10のパスと波長を表示する
    print("実行結果")
    for r in R:
        print('----------------------------')
        print(f"リクエスト{r}")
        print(f"(src,dest)={R[r]}")
        print(f"コアとリンク：{path[r]}")
        print(f"波長：{w_alloc[r]}")
    

    ## 同一のリンクを使いながら波長が重なっているペアが存在するかを確認する
    R_visited = set()
    for r1 in set(R.keys()):
        R_visited.add(r1)
        for r2 in set(R.keys())-R_visited:
            if not path[r1].isdisjoint(path[r2]):
                print('---------------------------------------')
                print(f"({r1}, {r2}) is unacceptable pare.")
                print(f"リクエスト{r1}")
                print(f"コアとリンク：{path[r1]}")
                print(f"波長：{w_alloc[r1]}")
                print(f"リクエスト{r2}")
                print(f"コアとリンク：{path[r2]}")
                print(f"波長：{w_alloc[r2]}")

    return


def check_error_rate():
    # リクエストの数
    R_number = 40
    # 試行回数
    number_of_running = 20
    # モデル
    model = MODEL_RCWA[0]
    # ネットワークトポロジー
    graph,topology_name = get_topology(topology_number=1)
    # 誤答回数のカウンター
    error_counter = 0

    ## 実験環境の表示
    print('<実験情報>')
    print(f"ネットワークトポロジー名：{topology_name}")
    print(f"リクエストの数：{R_number}")
    print(f"モデルの名前：{model}")
    print(f"試行回数：{number_of_running}")

    ## 実行確認
    # 変更が反映されてない状態で実行してしまうのを防ぐために確認する
    var = input("実行を続けますか？[Y/n]：")
    if var == "Y":  pass
    else:   return

    # ノード集合からリクエストを生成するため
    V = set(graph.nodes)
    # 波長
    W_number = 30
    W = {i+1 for i in range(W_number)}
    # コアの集合
    C = {1, 2, 3, 4}
    # リクエストの集合
    R = {}


    ## 実行開始
    for i in tqdm(range(number_of_running), leave=False):
        ## リクエスト集合の初期化
        for r in range(1,R_number+1):
            # ノードリストの中から2つをランダムで選択する
            [src, dist] = rd.sample(list(V), 2)
            R[r] = (src, dist)

        ## モデルの実行
        if model in MODEL_RCWA:
            path,w_alloc = eval(model)(graph=graph, R=R, W=W, C=C, getPath=True)
        else:
            path,w_alloc = eval(model)(graph=graph, R=R, W=W, getPath=True)

        ## 同一のリンクを使いながら波長が重なっている回数をカウントする
        R_visited = set()
        error_flag = False
        for r1 in set(R.keys()):
            R_visited.add(r1)
            for r2 in set(R.keys())-R_visited:
                if not path[r1].isdisjoint(path[r2]):
                    error_flag = True
                    break
            if error_flag:
                error_counter += 1
                break

    ## 誤答率の算出と表示
    error_rate = error_counter / number_of_running * 100
    print(f"誤答率(%):{error_rate}")


check_solution()