import pandas as pd
from alphacast import Alphacast
import json

#with open ("queries/key.csv", "r") as f:
#    key = f.read()

#API_key = str(key)

API_key = "ak_InwypYyuGx9GQlWNUHDf"
alphacast = Alphacast(API_key)
# df_bonos_iamc = alphacast.datasets.dataset(7961).download_data("pandas").iloc[:,:-1]
df_bonos_iamc = alphacast.datasets.dataset(7961).download_data("pandas")
# df_bonos_iamc_json = alphacast.datasets.dataset(7961).download_data("json")
df_bonos_iamc_json = df_bonos_iamc.set_index("Fecha").to_json(orient = 'records')
df_bonos_iamc["year"] = df_bonos_iamc["Fecha"].apply(lambda x: pd.to_numeric(x[:4]))

df_pesos = df_bonos_iamc[df_bonos_iamc["Moneda"]=="pesos"]
df_dolares = df_bonos_iamc[df_bonos_iamc["Moneda"]=="dolares"]
list_tickers = list(df_bonos_iamc["Codigo"].drop_duplicates())
