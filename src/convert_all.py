
import mlrun
import pandas as pd

@mlrun.handler()
def convert_all(context, source_url_base: str):
    # direct processing, no actions required
    for ds_name in ["azioni", "campi", "macroambiti", "piani", "tassonomia"]:
        source_url = source_url_base + ds_name + ".txt"
        input_data = mlrun.get_dataitem(source_url)
        df = input_data.as_df(format="csv", encoding="windows-1251", delimiter=";")
        df.reset_index(drop=True, inplace=True)
        context.log_dataset(ds_name, df=df, index=False)

    # comuni: process name and dates
    source_url = source_url_base + "comuni" + ".txt"
    input_data = mlrun.get_dataitem(source_url)
    df = input_data.as_df(format="csv", encoding="windows-1251", delimiter=";")
    df["comune"] = df["NomeOrganizzazione"].str.replace("COMUNE DI ", "").str.upper()
    df["Data_det_assegnazione"] = pd.to_datetime(df["Data_det_assegnazione"], format="%d/%m/%Y %H:%M:%S", errors="ignore")
    df["Data_det_revoca"] = df["Data_det_revoca"].fillna("")
    df["Data_det_revoca"] = pd.to_datetime(df["Data_det_revoca"], format="%d/%m/%Y %H:%M:%S", errors="ignore")
    df.reset_index(drop=True, inplace=True)
    context.log_dataset("comuni", df=df, index=False)

    # valutazioni: process dates
    source_url = source_url_base + "valutazioni" + ".txt"
    input_data = mlrun.get_dataitem(source_url)
    df = input_data.as_df(format="csv", encoding="windows-1251", delimiter=";")
    df["data_pub"] = pd.to_datetime(df["data_pub"], format="%d/%m/%Y %H:%M:%S", errors="ignore")
    df.reset_index(drop=True, inplace=True)
    context.log_dataset("valutazioni", df=df, index=False)

