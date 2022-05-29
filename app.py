from fastapi import FastAPI, HTTPException
import json
import pandas as pd
from queries.data import df_bonos_iamc_json, df_bonos_iamc, df_pesos, df_dolares, list_tickers

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


@app.get('/')
def welcome_api():
    return "Welcome to API from IAMC_Bonds"

@app.get('/bonos')
def get_all_bonds():       
    return df_bonos_iamc_json

@app.get('/bonos/{codigo}')
def get_bond(codigo:str):        
    df = df_bonos_iamc[df_bonos_iamc["Codigo"]==codigo]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono no encontrado")

@app.get('/bonos/moneda/{moneda}/{size}')
def get_currency_bond(moneda:str, size:int= 100):    
    if moneda=="pesos":        
        df = df_pesos.iloc[:size]
        if len (df)!=0:            
            js = json.loads(df.to_json(orient = 'records'))            
            return js
    elif moneda=="dolares":        
        df = df_dolares.iloc[:size]
        if len (df)!=0:            
            js = json.loads(df.to_json(orient = 'records'))            
            return js
    raise HTTPException(status_code=404, detail="Moneda no encontrada")  
           
@app.get('/bonos/tickers')
def get_tickers():       
    return list_tickers 


