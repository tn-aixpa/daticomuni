
import pandas as pd
import numpy as np

file_basepath = "daticomuni"

def convert_aziendali(project, source_artifact):
    converters={
        '2024_06_25 PIANI AZIENDALI': {'IDorganizzazione': np.int64, 'ANNUALITA': np.int64, 'Versione': np.int64, 'AnnoCompilazione': np.int64, 'CodiceCampoAzione': np.int64, 'CodiceTassonomiaAzione': np.int64, 'BeneF': np.int64, 'BeneM': np.int64, 'IDdettaglioAccorpamento': np.int64},
        'NuovaTassonomia': {},
        'T_NuovaTassonomia_DettaglioRev': {},
    }

    data_dir = f"{file_basepath}/data"
    try:
        shutil.rmtree(data_dir)
    except:
        print("Error deleting data dir")
                
    # Create the directory for the data
    if not path.exists(data_dir):
        makedirs(data_dir)
        
    try:
        archiveFile =source_artifact.download(data_dir) # this must change in the function
        with zipfile.ZipFile(archiveFile, 'r') as zip_ref:
            zip_ref.extractall(data_dir)    
    except:
        print("Error downloading data")
        
    for ds_name in ["2024_06_25 PIANI AZIENDALI", "NuovaTassonomia", "T_NuovaTassonomia_DettaglioRev"]:
        source_url = data_dir + '/' + ds_name + ".xlsx"
        df = pd.read_csv(source_url, encoding="windows-1251", delimiter=";")
        # df = pd.read_excel(input_data.get(), sheet_name=0, header=0, converters=converters[ds_name])
        df.reset_index(drop=True, inplace=True)
         project.log_dataitem(ds_name, data=df, kind='table', index=False)        

