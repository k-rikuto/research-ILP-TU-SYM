from gurobipy import Var

'''
数理モデルが求めた全ての解をdict[request_num : dict["Request" : (src,dist), "Path" : パス集合, "Wavelength" : 波長インデックス]]のデータベース形式に変換する関数

'''
def convert_vars_to_data(alpha:dict[tuple[int,tuple[int,int],int,int],Var], E_DIR:set[tuple[int,int]], R:dict[int,tuple[int,int]], W:set[int], C:set[int]) -> dict[int,dict[str,tuple[int,int]|set[tuple[int,int,int]]|int]]:

    data = {}

    # 変数alphaから(リンク,コア)と波長を抽出し、辞書に保存する
    for r_num,r in R.items():
        # wavelength, pathの初期化
        wavelength = 0
        path:set[tuple[int,int,int]] = set()

        path_flag = False # wavelengthのループを抜けるためのフラグ
        for e in E_DIR:
            # wavelengthが決まっているときwのループを省く
            if wavelength:
                for c in C:
                    if alpha[r_num,e,wavelength,c] > 0.8:
                        (u,v)=e
                        path.add((u,v,c))
                        break
            # wavelengthが決まっていないときwavelenghtも探索  
            else:
                for w in W:
                    if path_flag: break
                    for c in C:
                        if alpha[r_num,e,w,c] > 0.8:
                            (u,v)=e
                            path_flag = True
                            path.add((u,v,c))
                            wavelength = w
                            break
        
        data[r_num] = {"Request":r, "Path":path, "Wavelength":wavelength}

    return data