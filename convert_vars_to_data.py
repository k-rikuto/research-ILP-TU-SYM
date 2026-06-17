from gurobipy import Var

'''
数理モデルが求めた全ての解をdict[request_num : dict["Request" : (src,dest), "Path" : パス集合, "Wavelength" : 波長インデックス]]のデータベース形式に変換する関数

'''
def convert_vars_to_data(alpha:dict[tuple[int,tuple[int,int],int,int],Var], E_DIR:set[tuple[int,int]], R:dict[int,tuple[int,int]], W:set[int], C:set[int]=set({})) -> dict[int,tuple[tuple[int,int],set[tuple[int,int,int]],int]]:

    data = {}

    # 変数alphaから(リンク,コア)と波長を抽出し、辞書に保存する
    for r_num,r in R.items():
        # wavelength, pathの初期化
        wavelength = 0
        path:set[tuple[int,int,int]] = set()

        path_flag = False # wavelengthのループを抜けるためのフラグ
        for e in E_DIR:

            if len(C) > 0:
                # wavelengthが決まっているときwのループを省く
                if wavelength:
                    for c in C:
                        if alpha[r_num,e,wavelength,c].X > 0.8:
                            (u,v)=e
                            path.add((u,v,c))
                            break
                # wavelengthが決まっていないときwavelenghtも探索  
                else:
                    for w in W:
                        if path_flag: break
                        for c in C:
                            if alpha[r_num,e,w,c].X > 0.8:
                                (u,v)=e
                                path_flag = True
                                path.add((u,v,c))
                                wavelength = w
                                break
            else:
                # wavelengthが決まっているときwのループを省く
                if wavelength:
                    if alpha[r_num,e,wavelength].X > 0.8:
                        (u,v)=e
                        path.add((u,v,1))
                # wavelengthが決まっていないときwavelenghtも探索  
                else:
                    for w in W:
                        if alpha[r_num,e,w].X > 0.8:
                            (u,v)=e
                            path.add((u,v,1))
                            wavelength = w
                            break
                            
        
        data[r_num] = (r, path, wavelength)

    return data