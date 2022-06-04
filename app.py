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

app = FastAPI(title="API bonos IAMC (base=2016)", 
              description= "Obtencion de información sobre bonos argentinos listados en IAMC",
              version= "0.0.1",
              openapi_tags=tags_metadata
                )


@app.get('/')
def welcome_api():
    return "Welcome to API from IAMC_Bonds"

@app.get('/tickers')
def get_tickers():
    """
        Obtención de los códigos correspondientes a cada unos de los bonos del dataset
    """       
    return list_tickers

@app.get('/bonos')
def get_all_bonds():
    """
        Obtención de toda la serie correspondiente a la totalidad de los bonos del dataset
    """        
    return df_bonos_iamc_json

@app.get('/bonos/{codigo}')
def get_bond(codigo:str):
    """
        Obtención de la información correspondiente al bono seleccionado en base a su codigo
    """        
    df = df_bonos_iamc[df_bonos_iamc["Codigo"]==codigo]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono no encontrado")

@app.get('/bonos/fecha/{year}')
def get_bond_by_year(year:int):
    """
        Obtención de toda la serie correspondiente a los bonos, filtrado de acuerdo al año
        seleccionado
    """        
    df = df_bonos_iamc[df_bonos_iamc["Fecha"].str.startswith(str(year))]    
    if len (df)!=0:
        # js =  json.loads(df.to_json(orient = 'records'))
        # return js
        return df
    raise HTTPException(status_code=404, detail="Bono no encontrado")

@app.get('/bonos/moneda/{moneda}/{size}')
def get_bond_by_currency(moneda:str, size:int= 100):
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
           
 


