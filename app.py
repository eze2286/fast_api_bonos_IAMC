from fastapi import FastAPI, HTTPException
import json
import pandas as pd
from queries.data import df_bonos_iamc_json, df_bonos_iamc, df_pesos, df_dolares, list_tickers

tags_metadata = [
  {
    "name": "bonos",
    "description": "bonos endpoint",
    "externalDocs": {
            "description": "Fuente: IAMC",
            "url": "https://www.alphacast.io/datasets/7961",
        }, 
  }
]

app = FastAPI(title="API bonos IAMC (base=2011)", 
              description= "Obtencion de información sobre bonos argentinos listados en IAMC",
              version= "0.0.1",
              openapi_tags=tags_metadata
                )


@app.get('/', tags=["Welcome"])
async def welcome_api():
    return "Welcome to API from IAMC_Bonds"

@app.get('/tickers', tags=["Tickers"])
async def get_tickers():
    """
        Obtención de los códigos correspondientes a cada unos de los bonos del dataset
    """       
    return list_tickers

@app.get('/bonos', tags=["All Data"])
async def get_all_bonds():
    """
        Obtención de toda la serie correspondiente a la totalidad de los bonos del dataset
    """        
    return df_bonos_iamc_json

@app.get('/bonos/{codigo}', tags=["Bonds by Ticker"])
async def get_bond(codigo:str):
    """
        Obtención de la información correspondiente al bono seleccionado en base a su codigo
    """        
    df = df_bonos_iamc[df_bonos_iamc["Codigo"]==codigo]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono no encontrado")

@app.get('/bonos/data/{codigo}/{year}', tags=["Bonds by Ticker and Year"])
async def get_bond_by_tick_year(codigo:str, year:int):
    """
        Obtención de la información correspondiente al bono seleccionado en base a su codigo y año
    """        
    df = df_bonos_iamc[(df_bonos_iamc["Codigo"]==codigo) & (df_bonos_iamc["year"]==year)]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono o año no encontrado")

@app.get('/bonos/year/{year}', tags=["Bonds by Year"])
async def get_bond_by_year(year:int):
    """
        Obtención de toda la serie correspondiente a los bonos, filtrado de acuerdo al año
        seleccionado
    """        
    df = df_bonos_iamc[df_bonos_iamc["year"]==year]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js        
    raise HTTPException(status_code=404, detail="Fecha no encontrada")

@app.get('/bonos/moneda/{moneda}/{size}', tags=["Bonds by Currency and Size"])
async def get_bond_by_currency(moneda:str, size:int= 100):
    """
        Obtención de la información correspondiente a cada bono en base a la moneda (pesos/dolares)
        seleccionada como parametro. Adiionalmente se debe pasar como parámetro un size (ejemplo 100)
        para indicar la cantidad de datos a visualizar.
    """    
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
           
 


