import pandas as pd
from alphacast import Alphacast
from password import API_key
import json

alphacast = Alphacast(API_key)
df_bonos_iamc = alphacast.datasets.dataset(7961).download_data("pandas").iloc[:,:-1]
df_bonos_iamc_json = alphacast.datasets.dataset(7961).download_data("json")
