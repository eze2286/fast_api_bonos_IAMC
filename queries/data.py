import pandas as pd
from alphacast import Alphacast
import json

API_key = "ak_InwypYyuGx9GQlWNUHDf"
alphacast = Alphacast(API_key)
df_bonos_iamc = alphacast.datasets.dataset(7961).download_data("pandas").iloc[:,:-1]
df_bonos_iamc_json = alphacast.datasets.dataset(7961).download_data("json")
df_pesos = df_bonos_iamc[df_bonos_iamc["Moneda"]=="pesos"]
df_dolares = df_bonos_iamc[df_bonos_iamc["Moneda"]=="dolares"]

