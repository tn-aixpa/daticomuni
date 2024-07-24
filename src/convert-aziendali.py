
import mlrun
import pandas as pd
import numpy as np

@mlrun.handler()
def convert_aziendali(context, source_url_base: str):
    converters={
        '2024_06_25 PIANI AZIENDALI': {'IDorganizzazione': np.int64, 'ANNUALITA': np.int64, 'Versione': np.int64, 'AnnoCompilazione': np.int64, 'CodiceCampoAzione': np.int64, 'CodiceTassonomiaAzione': np.int64, 'BeneF': np.int64, 'BeneM': np.int64, 'IDdettaglioAccorpamento': np.int64},
        'NuovaTassonomia': {},
        'T_NuovaTassonomia_DettaglioRev': {},
    }

    for ds_name in ["2024_06_25 PIANI AZIENDALI", "NuovaTassonomia", "T_NuovaTassonomia_DettaglioRev"]:
        source_url = source_url_base + ds_name + ".xlsx"
        input_data = mlrun.get_dataitem(source_url)
        df = pd.read_excel(input_data.get(), sheet_name=0, header=0, converters=converters[ds_name])
        df.reset_index(drop=True, inplace=True)
        context.log_dataset(ds_name, df=df, index=False)
