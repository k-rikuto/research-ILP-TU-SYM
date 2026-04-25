import pandas as pd
import os

def analyze_request(R_list_list:list[list[tuple[int,int]]], V:set, file:str):
    
    R_set = []
    R_set_str = []
    V_src = V.copy()
    V_dist = V.copy()
    for src in V_src:
        V_dist -= {src}
        for dist in V_dist:
            R_set.append((src,dist))
            R_set_str.append(f"({src},{dist})")
    
    r_num_init = {r:0 for r in R_set}
    r_num = r_num_init.copy()
    r_num_list = []
    times = 0
    times_list = []

    for R_list in R_list_list:
        times += 1
        times_list.append(times)
        for r in R_list:
            src, dist = r
            if src < dist:  r_num[(src,dist)] += 1
            else:   r_num[(dist,src)] += 1
        r_num_list.append(list(r_num.values()))
        r_num = r_num_init.copy()

    request_df = pd.DataFrame(r_num_list, index=times_list, columns=R_set_str)

    # Excelに書き込み
    with pd.ExcelWriter(file, mode='a') as writer:
        request_df.to_excel(writer, sheet_name='request')
    

        