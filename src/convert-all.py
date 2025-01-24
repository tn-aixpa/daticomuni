
import pandas as pd
from os import path, makedirs
import zipfile
        
file_basepath = "daticomuni"

def convert_all(project, source_artifact):
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
        
           
    for ds_name in ["azioni", "campi", "macroambiti", "piani", "tassonomia"]:
        source_url = data_dir + '/' + ds_name + ".txt"        
        df = pd.read_csv(source_url, encoding="windows-1251", delimiter=";")
        df.reset_index(drop=True, inplace=True)
        project.log_dataitem(ds_name, data=df, kind='table', index=False)        

    # comuni: process name and dates
    source_url =  data_dir + '/' + "comuni" + ".txt"
    df = pd.read_csv(source_url, encoding="windows-1251", delimiter=";")
    df["comune"] = df["NomeOrganizzazione"].str.replace("COMUNE DI ", "").str.upper()
    df["Data_det_assegnazione"] = pd.to_datetime(df["Data_det_assegnazione"], format="%d/%m/%Y %H:%M:%S", errors="ignore")
    df["Data_det_revoca"] = df["Data_det_revoca"].fillna("")
    df["Data_det_revoca"] = pd.to_datetime(df["Data_det_revoca"], format="%d/%m/%Y %H:%M:%S", errors="ignore")
    df.reset_index(drop=True, inplace=True)
    project.log_dataitem("comuni", data=df, kind='table', index=False)

    # valutazioni: process dates
    source_url =  data_dir + '/' + "valutazioni" + ".txt"
    df = pd.read_csv(source_url, encoding="windows-1251", delimiter=";")
    df["data_pub"] = pd.to_datetime(df["data_pub"], format="%d/%m/%Y %H:%M:%S", errors="ignore")
    df.reset_index(drop=True, inplace=True)
    project.log_dataitem("valutazioni", data=df, kind='table', index=False)
