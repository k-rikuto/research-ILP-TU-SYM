import pandas as pd


def results_to_excel(results:dict[str, list[tuple[float, float]]], number_of_runnning:int, topology_name:str, R_number:int, isRWA=False):

    runtime_data = []
    wavelength_data = []

    for i in range(number_of_runnning+1):
        r_list = []
        w_list = []

        for model in results:
            runtime,wavelength = results[model][i]
            r_list.append(runtime)
            w_list.append(wavelength)
        
        runtime_data.append(r_list)
        wavelength_data.append(w_list)
    
    model_list = list(results)
    time_list = list(range(1,number_of_runnning+1))
    time_list.append('Average')

    runtime_df = pd.DataFrame(runtime_data, index=time_list, columns=model_list)
    wavelength_df = pd.DataFrame(wavelength_data, index=time_list, columns=model_list)

    # Excelに書き込み

    if isRWA:
        with pd.ExcelWriter(f'results/RWA/{topology_name}/results_request_{R_number}.xlsx') as writer:
            runtime_df.to_excel(writer, sheet_name='runtime')
            wavelength_df.to_excel(writer, sheet_name='wavelength')
    else:
        with pd.ExcelWriter(f'results/{topology_name}/results_request_{R_number}.xlsx') as writer:
            runtime_df.to_excel(writer, sheet_name='runtime')
            wavelength_df.to_excel(writer, sheet_name='wavelength')
