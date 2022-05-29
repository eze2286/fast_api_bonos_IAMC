from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
import json
import pandas as pd
from queries.data import df_bonos_iamc_json, df_bonos_iamc, df_pesos, df_dolares, df_pesos_json, df_dolares_json
# from alphacast import Alphacast
# from password import API_key
# import json

tags_metadata = [
  {
    "name": "bonos",
    "description": "bonos endpoint"
  }
]

app = FastAPI(title="API bonos IAMC (base=2017)", 
              description= "Obtencion de información sobre bonos argentinos listados en IAMC",
              version= "0.0.1",
              openapi_tags=tags_metadata
                )

# alphacast = Alphacast(API_key)
# df_bonos_iamc = alphacast.datasets.dataset(7961).download_data("pandas").iloc[:,:-1]



@app.get('/')
def welcome_api():
    return "Welcome to API from IAMC_Bonds"

@app.get('/bonos')
def get_all_bonds():
    # df_bonos_iamc_json = alphacast.datasets.dataset(7961).download_data("json")   
    return df_bonos_iamc_json

@app.get('/bonos/{codigo}')
def get_bond(codigo:str):        
    df = df_bonos_iamc[df_bonos_iamc["Codigo"]==codigo].set_index("Fecha")    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono no encontrado")

@app.get('/bonos/moneda/{moneda}')
def get_currency_bond(moneda:str):        
    # df = df_bonos_iamc[df_bonos_iamc["Moneda"]==moneda].set_index("Fecha")
    if moneda=="pesos":
        # df = df_bonos_iamc[df_bonos_iamc["Moneda"]=="pesos"].set_index("Fecha")
        df = df_pesos
        if len (df)!=0:
            # js =  json.loads(df.to_json(orient = 'records'))
            js = df_pesos_json            
            return js
    elif moneda=="dolares":
        # df = df_bonos_iamc[df_bonos_iamc["Moneda"]=="dolares"].set_index("Fecha")
        df = df_dolares
        if len (df)!=0:
            # js =  json.loads(df.to_json(orient = 'records'))
            js = df_dolares_json            
            return js

    raise HTTPException(status_code=404, detail="Moneda no encontrada")  
           
    


