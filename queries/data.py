import pandas as pd
from alphacast import Alphacast
# from password import API_key
import json

API_key = "ak_InwypYyuGx9GQlWNUHDf"
alphacast = Alphacast(API_key)
df_bonos_iamc = alphacast.datasets.dataset(7961).download_data("pandas").iloc[:,:-1]
df_bonos_iamc_json = alphacast.datasets.dataset(7961).download_data("json")
df_pesos = df_bonos_iamc[df_bonos_iamc["Moneda"]=="pesos"].set_index("Fecha")
df_dolares = df_bonos_iamc[df_bonos_iamc["Moneda"]=="dolares"].set_index("Fecha")
df_pesos_json= json.loads(df_pesos.to_json(orient = 'records'))
df_dolares_json= json.loads(df_dolares.to_json(orient = 'records'))
